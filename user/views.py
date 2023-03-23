from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from rest_framework import status
import pytesseract
from PIL import Image
import re
from .extracts import *
from passporteye import read_mrz
import os
from .models import id_data
from .converter import pdf_to_image

# from .preprocess import preprocess_image

# Create your views here.



class RegiserView(APIView):
    """
    API View for user registration and id_document extraction and saving.
    """
     
    def post(self,request):
        """
        saves user provided details and transfer id_document for extraction
        """
        serializer = UserRegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            doc_save = self.save_document_data(request,userid=user.id)
            if doc_save == True:
                return Response({"message":"saved successfully","status":True},status=status.HTTP_201_CREATED)
            else :
                user.delete()
                return Response({"message":doc_save,"status":False},status=status.HTTP_406_NOT_ACCEPTABLE)

        return Response({"message":serializer.errors,"status":False},status=status.HTTP_406_NOT_ACCEPTABLE)
    

    def save_document_data(self,request,userid):

        """
        Method to extract and save data from id_document image or pdf

        :return: True if document data saved successfully, otherwise serializer errors
        """

        image_file = request.FILES['id_proof']

        # If the file is a PDF, convert it to an image.
        if request.data['id_filetype'] == "pdf":
            if request.data['id_type'] == "passport":
                return "scanning passport of pdf type is currently not supported"
            
            file = pdf_to_image(image_file)
            img = Image.frombytes("RGB", [file.width, file.height], file.samples)  # convert pixmap to PIL Image
            image_file = img
        else:
            image_file = Image.open(image_file)

        # Extract text from the image.
        text = pytesseract.image_to_string(image_file)

        # Extract data based on the type of document.
        id_type = request.data.get('id_type')
        id_name = ""
        id_no = ""
        id_dob = ""
        if id_type == "license" :
            id_name, id_dob = extract_from_licence(text)



        if id_type == "adhaar":
            id_name = extract_name_from_adhaar(text)
            id_no = extract_idno_from_adhaar(text)
            id_dob = extract_dob_from_adhaar(text)


        if id_type == "passport":
            id_name, id_no, id_dob = extract_data_from_passport(image_file)
            if id_name == "error":
                return "Error while scanning passport image.Ensure that uploaded image is a valid passport image and not bad quality"    

        data = {
                "userid": userid,
                "id_no":id_no,
                "id_dob":id_dob,
                "id_name":id_name,
                "id_fulldata":text,
                "id_type":id_type
                }
        
        serializer = DocumentSerializer(data=data,partial=True)

        if serializer.is_valid():
            serializer.save()
            return True
        return serializer.errors


class FetchUsers(APIView):
    """
    API View to fetch all users
    """
    def get(self,request):
        allusers = UserInfo.objects.all()
        serializer = DataFetchSerializer(allusers,many=True)
        return Response({"message":serializer.data,"status":True},status=status.HTTP_200_OK)


class FetchDocumentData(APIView):
    """
    API View to fetch data extracted using OCR for specific user
    """
    def get(self,request,id):
        data = id_data.objects.all()
        serializer = DocumentSerializer(data,many=True)
        return Response({"message":serializer.data,"status":True},status=status.HTTP_200_OK)
            
        
        
        
class NameMatchPercentage(APIView):
    """
    API View to get name match percentage with both case and noncase sensitivity
    """

    def get(self,request,givenname,id_name):

        string1 = givenname
        string2 = id_name
        
        len1 = len(string1)
        len2 = len(string2)
        count = 0

        if len1 >= len2 :
            max_len = len1
            min_len = len2
        else:
            max_len = len2
            min_len = len1
        
        for i in range(min_len):
            if string1[i] == string2[i]:
                count += 1

        case_percentage = (count / max_len) * 100


        string1_low = string1.lower()
        string2_low = string2.lower()

        count2 = 0
        for i in range(min_len):
            if string1_low[i] == string2_low[i]:
                count2 +=1

        noncase_percentage = (count2 / max_len ) * 100
        
        data = {
            "case_percentage":str(case_percentage),
            "noncase_percentage":str(noncase_percentage)
        }

        return Response(data)


    

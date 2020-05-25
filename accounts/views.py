from django.shortcuts import render, get_object_or_404
from rest_framework import views, generics, permissions, status
from rest_framework.response import Response
from .serializers import CustomerSerializer, VendorCreateSerializer, LoginSerializer, UserSerializer, SetPasswordSerializer
from knox.models import AuthToken
from .models import User
from django.core.mail import EmailMessage, send_mail
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login as django_login
EMAIL_HOST_USER = 'smtp.gmail.com'


def send_email(user):
    intro = 'Welcome To Food Vendor Application'
    message = """

        You're receiving this email because you need to finish 
        registration process on Food vendor Website.

        Please click on the link page to set your password:


    """
    warning = """

        This Link expires in 24 hours after which you'll be asked to reregister
    """
    subject = 'FVA || Set Password'
    url = 'http://localhost:8000/api/auth/set/password/user/' + \
        str(user.unique_ref)
    body = intro + message + url + warning
    recipient = [user.email]
    send_mail(subject, body, EMAIL_HOST_USER, recipient, fail_silently=False
              )


class VendorRegView(generics.CreateAPIView):

    """
        post:
        Create a new Vendor.
    """
    serializer_class = VendorCreateSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # send_email(user)
        # return Response({
        #     "message": "Vendor created succesfully",
        #     'vendor': serializer.data
        # }, status=status.HTTP_201_CREATED)
        try:
            send_email(user)
        except:
            user.delete()
            raise
        else:
            return Response({
                "message": "Vendor created succesfully",
                'vendor': serializer.data
            }, status=status.HTTP_201_CREATED)


class CustomerRegView(generics.CreateAPIView):
    """
        post:
        Create a new Customer taking first Name, last Name, phone Number and  
        email  as  request.
    """
    serializer_class = CustomerSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        try:
            send_email(user)
        except:
            user.delete()
            raise
        else:
            return Response({
                "message": "Vendor created succesfully, check your mail to set password",
                'customer': serializer.data
            }, status=status.HTTP_201_CREATED)


class UserLogin(generics.GenericAPIView):
    """
    post:
    Login users using email and password as parameters.
    """
    serializer_class = LoginSerializer

    @csrf_exempt
    def post(self, request):
        email = request.data['email']
        user = User.objects.get(email=email)
        if not user.isConfirmed:
            return Response({
                'message': 'User has not set password, check your mail for instruction'
            }, status=status.HTTP_403_FORBIDDEN)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        django_login(request, user)
        token = AuthToken.objects.create(user)[1]
        return Response({
            "message": "Login succesfully",
            'user': serializer.data,
            'token': token
        }, status=status.HTTP_201_CREATED)


def cal_delay(expired_date, returned_date):
    delay = returned_date - expired_date
    return delay.days


class SetPasswordAPI(generics.UpdateAPIView):
    """
    put:
    password set api taking in unique_ref of users in the path parameters
    """
    serializer_class = SetPasswordSerializer
    queryset = User.objects.all()

    def put(self, request, unique_ref):
        user = get_object_or_404(User, unique_ref=unique_ref)
        password = request.data['password']

        if user.isConfirmed:
            return Response({
                'message': 'user already set password'
            }, status=status.HTTP_403_FORBIDDEN)
        else:
            now = timezone.now()
            delay = cal_delay(user.create_date, now)
            if delay >= 1:
                user.delete()
                return Response({
                    "message": "Link has expired. Reregister the email"
                }, status=status.HTTP_410_GONE)
            user.isConfirmed = True
            user.set_password(password)
            user.save()
            token = AuthToken.objects.create(user)[1]
            return Response({
                'message': 'password succesfully set',
                'user': UserSerializer(user).data,
                'token': token
            })

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import User, Post, Tag
import json

# Create your views here.

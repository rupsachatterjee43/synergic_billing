from fastapi import APIRouter
from models.master_model import createResponse
from models.masterApiModel import db_select, db_Insert
# from models.admin_form_model import 

settingsRouter = APIRouter()
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import CreateView, ListView, TemplateView, UpdateView
import crm.models as models
from django.urls import reverse_lazy
from django.db.models.signals import post_save
from django.dispatch import receiver
from crm.forms import EmployeeForm, UserForm, CompanyForm
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext as _
from crm.forms import OpportunityForm, RegisterUserForm
from crm.serializers import CompanySerializer, OpportunitySerializer
from rest_framework import viewsets

class IndexView(TemplateView):
    template_name = "index.html"

class CompanyCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = "company/create_company.html"
    form_class  = CompanyForm
    success_url = reverse_lazy("index")
    # Translators: This message is shown after successful creation of a company
    success_message = _("Company created!")

class CompanyListView(LoginRequiredMixin, ListView):
    model = models.Company
    template_name = "company/list_company.html"

class OpportunityListView(LoginRequiredMixin, ListView):
    model = models.Opportunity
    template_name = "opportunity/list_opportunity.html"

class OpportunityCreateView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'crm.add_opportunity'
    template_name = "company/create_company.html"
    form_class = OpportunityForm
    success_url = reverse_lazy("index")
    success_message = "Opportunity created!"

class OpportunityUpdateView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    form_class = OpportunityForm
    template_name = "opportunity/update_opportunity.html"
    success_url = reverse_lazy("index")
    success_message = "Opportunity updated!"


class EmployeeUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = "employee/update_employee.html"
    fields = ['department', 'phone_number', "office_number", "manager"]
    success_url = reverse_lazy("employee_update")
    success_message = "Data was updated successfully!"

    def get_object(self, queryset=None):
        return self.request.user.employee


class RegisterView(CreateView):
    form_class = RegisterUserForm
    success_url = reverse_lazy("login")
    template_name = "registration/register.html"


class OpportunityViewSet(viewsets.ModelViewSet):
    queryset = models.Opportunity.objects.all()
    serializer_class = OpportunitySerializer

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = models.Company.objects.all()
    serializer_class = CompanySerializer

from django.views import generic
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse_lazy
from .models import daily_log, weekly_report
from .forms import UserForm
from django.shortcuts import HttpResponseRedirect, get_list_or_404


class CreateDay(CreateView):

    model = daily_log
    fields = ['start_date', 'start_time', 'end_time', 'lunch_time', 'travel_time', 'extra_time', 'week', 'comments']

    def get_initial(self):
        print(self.kwargs['pk'])
        initial = super(CreateDay, self).get_initial()
        initial['week'] = self.kwargs['pk']
        return initial

    def get_form(self, form_class=None):
        form = super(CreateDay, self).get_form()
        form.fields['start_date'].widget.attrs.update({'id': 'datepicker', 'class': 'form-control'})
        form.fields['start_time'].widget.attrs.update({'id': 'timepicker', 'class': 'form-control'})
        form.fields['end_time'].widget.attrs.update({'id': 'timepicker1', 'class': 'form-control'})
        form.fields['week'].widget.attrs.update({'id': 'selectweek', 'class': 'form-control'})
        form.fields['lunch_time'].widget.attrs.update({'class': 'form-control'})
        form.fields['travel_time'].widget.attrs.update({'class': 'form-control'})
        form.fields['extra_time'].widget.attrs.update({'class': 'form-control'})
        form.fields['comments'].widget.attrs.update({'class': 'form-control'})
        return form

    def form_valid(self, form):
        return_url = '/report/week/' + self.kwargs['pk']
        self.object = form.save()
        return HttpResponseRedirect(return_url)


class UpdateDay(UpdateView):
    model = daily_log
    fields = ['start_date', 'start_time', 'end_time', 'lunch_time', 'travel_time', 'extra_time', 'week', 'comments']

    def get_form(self, form_class=None):
        form = super(UpdateView, self).get_form()
        form.fields['start_date'].widget.attrs.update({'id': 'datepicker', 'class': 'form-control'})
        form.fields['start_time'].widget.attrs.update({'id': 'timepicker', 'class': 'form-control'})
        form.fields['end_time'].widget.attrs.update({'id': 'timepicker1', 'class': 'form-control'})
        form.fields['week'].widget.attrs.update({'id': 'selectweek', 'class': 'form-control'})
        form.fields['lunch_time'].widget.attrs.update({'class': 'form-control'})
        form.fields['travel_time'].widget.attrs.update({'class': 'form-control'})
        form.fields['extra_time'].widget.attrs.update({'class': 'form-control'})
        form.fields['comments'].widget.attrs.update({'class': 'form-control'})
        return form

    def form_valid(self, form):
        return_url = '/report/week/' + self.kwargs['week']
        self.object = form.save()
        return HttpResponseRedirect(return_url)

class DeleteDay(DeleteView):
    model = daily_log

    def delete(self, request, *args, **kwargs):
        return_url = '/report/week/' + self.kwargs['week']
        self.object = self.get_object()
        self.object.delete()
        return HttpResponseRedirect(return_url)


class UserFormView(generic.View):
    form_class = UserForm
    template_name = 'registration_form.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form':form})


    def post(self, request):

        form = self.form_class(request.POST)
        if form.is_valid():
            #user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            #user.set_password(password)
            #user.save()
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('report:view_home')

        return render(request, self.template_name, {'form': form})


class WeekListView(generic.ListView):
    template_name = 'week.html'

    def get_queryset(self):
        return weekly_report.objects.all()


class CreateWeek(CreateView):
    model = weekly_report
    fields = ['name', 'sent', 'total_miscelaneous', 'comments']

    def get_form(self, form_class=None):
        form = super(CreateWeek, self).get_form()
        form.fields['name'].widget.attrs.update({'id': 'datepicker', 'autocomplete': 'off', 'class': 'form-control'})
        form.fields['sent'].widget.attrs.update({'id': 'datepicker', 'class': 'form-control'})
        form.fields['total_miscelaneous'].widget.attrs.update({'id': 'timepicker', 'class': 'form-control'})
        form.fields['comments'].widget.attrs.update({'id': 'timepicker1', 'class': 'form-control'})
        return form


class DeleteWeek(DeleteView):
    model = weekly_report
    success_url = reverse_lazy('report:view_weeks')


class UpdateWeek(UpdateView):
    model = weekly_report
    fields = ['name', 'sent', 'total_hours', 'total_miscelaneous', 'comments']


def WeekDetailView(request, pk):

    hours = 0

    week = weekly_report.objects.filter(id=pk)
    days_in_week = daily_log.objects.filter(week=pk)

    for item in week:
        name = item.name
        sent = item.sent
        week_id = item.id
        total_miscelaneous = item.total_miscelaneous
        comments = item.comments

    for day in days_in_week:
        hours += day.hours_worked

    updated_hours = weekly_report.objects.get(id=pk)
    updated_hours.total_hours = hours
    updated_hours.save()

    context = {'week':week, 'comments':comments, 'total_miscelaneous': total_miscelaneous, 'sent': sent, 'name': name, 'days_in_week': days_in_week, 'hours': hours, 'week_id': week_id}
    return render(request, 'week_detail.html', context)

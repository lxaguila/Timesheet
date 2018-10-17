from django.views import generic
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse_lazy
from .models import daily_log, weekly_report
from .forms import UserForm
from django.shortcuts import HttpResponseRedirect, HttpResponse
from django.http import Http404


class CreateDay(CreateView):

    model = daily_log
    fields = ['start_date', 'start_time', 'end_time', 'lunch_time', 'travel_time', 'extra_time', 'comments']

    def get_form(self, form_class=None):
        form = super(CreateDay, self).get_form()
        form.fields['start_date'].widget.attrs.update({'id': 'datepicker', 'class': 'form-control'})
        form.fields['start_time'].widget.attrs.update({'id': 'timepicker', 'class': 'form-control'})
        form.fields['end_time'].widget.attrs.update({'id': 'timepicker1', 'class': 'form-control'})
        form.fields['lunch_time'].widget.attrs.update({'class': 'form-control'})
        form.fields['travel_time'].widget.attrs.update({'class': 'form-control'})
        form.fields['extra_time'].widget.attrs.update({'class': 'form-control'})
        form.fields['comments'].widget.attrs.update({'class': 'form-control'})
        return form

    def form_valid(self, form):
        pk = int(self.kwargs['pk'])
        print(pk)
        form.instance.week_id = pk
        return_url = '/report/week/' + self.kwargs['pk']
        self.object = form.save()
        return HttpResponseRedirect(return_url)


class UpdateDay(UpdateView):
    model = daily_log
    fields = ['start_date', 'start_time', 'end_time', 'lunch_time', 'travel_time', 'extra_time', 'comments']

    def get_queryset(self):
        user_id = weekly_report.objects.filter(author=self.request.user)
        id = (user_id.values_list('id', flat=True)[0])
        return daily_log.objects.filter(week=id)



    def get_form(self, form_class=None):
        form = super(UpdateView, self).get_form()
        form.fields['start_date'].widget.attrs.update({'id': 'datepicker', 'class': 'form-control'})
        form.fields['start_time'].widget.attrs.update({'id': 'timepicker', 'class': 'form-control'})
        form.fields['end_time'].widget.attrs.update({'id': 'timepicker1', 'class': 'form-control'})
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
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('report:view_weeks')

        return render(request, self.template_name, {'form': form})


class WeekListView(generic.ListView):
    template_name = 'week.html'

    def get_queryset(self):
        return weekly_report.objects.filter(author=self.request.user)


class CreateWeek(CreateView):
    model = weekly_report
    fields = ['name', 'sent', 'miscelaneous', 'comments']

    def get_form(self, form_class=None):
        form = super(CreateWeek, self).get_form()
        form.fields['name'].widget.attrs.update({'id': 'datepicker', 'autocomplete': 'off', 'class': 'form-control'})
        form.fields['sent'].widget.attrs.update({'class': 'form-control', 'id': 'check_week'})
        form.fields['miscelaneous'].widget.attrs.update({'class': 'form-control'})
        form.fields['comments'].widget.attrs.update({'class': 'form-control'})
        return form

    def form_valid(self, form):
         user_id = self.request.user
         form.instance.author = user_id
         return super(CreateWeek, self).form_valid(form)

class DeleteWeek(DeleteView):
    model = weekly_report
    success_url = reverse_lazy('report:view_weeks')


class UpdateWeek(UpdateView):
    model = weekly_report
    fields = ['name', 'sent', 'total_hours', 'miscelaneous', 'comments']

    def get_queryset(self):
        return weekly_report.objects.filter(author=self.request.user)

    def form_valid(self, form):
        return_url = '/report/week/' + self.kwargs['pk']
        self.object = form.save()
        return HttpResponseRedirect(return_url)


def WeekDetailView(request, pk):

    hours = 0

    week = weekly_report.objects.filter(id=pk, author=request.user)

    if week:

        days_in_week = daily_log.objects.filter(week=pk)

        for item in week:
            name = item.name
            sent = item.sent
            week_id = item.id
            miscelaneous = item.miscelaneous
            comments = item.comments

        for day in days_in_week:
            hours += day.hours_worked

        updated_hours = weekly_report.objects.get(id=pk)
        updated_hours.total_hours = hours
        updated_hours.save()

        context = {'week':week, 'comments':comments, 'miscelaneous': miscelaneous, 'sent': sent, 'name': name, 'days_in_week': days_in_week, 'hours': hours, 'week_id': week_id}
        return render(request, 'week_detail.html', context)

    else:
        raise Http404()

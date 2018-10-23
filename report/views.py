from django.views import generic
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse_lazy
from .models import daily_log, weekly_report
from django.shortcuts import HttpResponseRedirect, HttpResponse
from django.http import Http404
from report.forms import SignUpForm
from django.template.loader import render_to_string, get_template
from weasyprint import HTML, CSS
from django.conf import settings



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
        form.instance.week_id = pk
        return_url = '/report/week/' + str(pk)
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


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


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

    def get_queryset(self):
        return weekly_report.objects.filter(author=self.request.user)

    success_url = reverse_lazy('report:view_weeks')


class UpdateWeek(UpdateView):
    model = weekly_report
    fields = ['name', 'sent', 'miscelaneous', 'comments']


    def get_form(self, form_class=None):
        form = super(UpdateWeek, self).get_form()
        form.fields['name'].widget.attrs.update({'id': 'datepicker', 'autocomplete': 'off', 'class': 'form-control'})
        form.fields['sent'].widget.attrs.update({'class': 'form-control', 'id': 'check_week'})
        form.fields['miscelaneous'].widget.attrs.update({'class': 'form-control'})
        form.fields['comments'].widget.attrs.update({'class': 'form-control'})
        return form

    def get_context_data(self):
        add_context = {'week_id': self.kwargs['pk']}
        ctx = super(UpdateView, self).get_context_data()
        ctx.update(add_context)
        return ctx

    def get_queryset(self):
        return weekly_report.objects.filter(author=self.request.user)

    def form_valid(self, form):
        return_url = '/report/week/' + self.kwargs['pk']
        self.object = form.save()
        return HttpResponseRedirect(return_url)


def WeekDetailView(request, pk):

    try:
        week = weekly_report.objects.get(id=pk, author=request.user)
    except:
        raise Http404()

    try:
        print_option = (request.GET.get('print', ''))
    except:
        print('noprint')

    user = request.user
    name = week.name
    sent = week.sent
    week_id = week.id
    miscelaneous = week.miscelaneous
    comments = week.comments
    hours = week.miscelaneous

    days_in_week = daily_log.objects.filter(week=week_id)

    for day in days_in_week:
        hours += day.hours_worked

    week.total_hours = hours
    week.save()

    if print_option == "yes":
        context = {'user': user, 'week': week, 'comments': comments, 'miscelaneous': miscelaneous, 'sent': sent, 'name': name, 'days_in_week': days_in_week, 'hours': hours, 'week_id': week_id}
        content = render_to_string('print_week.html', context)
        html_read = HTML(string=content)
        result = html_read.write_pdf(target=None, stylesheets=[CSS('./static/stylesheet.css')], zoom=1, attachments=None, presentational_hints=False, font_config=None)
        response = HttpResponse(result, content_type='application/pdf')
        return response

    elif print_option == "preview":
        context = {'user': user, 'week': week, 'comments': comments, 'miscelaneous': miscelaneous, 'sent': sent, 'name': name, 'days_in_week': days_in_week, 'hours': hours, 'week_id': week_id}
        return render(request, 'print_week.html', context)

    else:
        context = {'week':week, 'comments':comments, 'miscelaneous': miscelaneous, 'sent': sent, 'name': name, 'days_in_week': days_in_week, 'hours': hours, 'week_id': week_id}
        return render(request, 'week_detail.html', context)





from .models import Car, Repair
from django.views.generic import ListView, UpdateView, DeleteView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages


class AddCarView(LoginRequiredMixin, CreateView):
    model = Car
    fields = ['make', 'model', 'vrn', 'year']
    success_url = '/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class AddRepairView(LoginRequiredMixin, CreateView):
    model = Repair
    fields = ['date', 'description']
    success_message = 'New repair has been added'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['car'] = Car.objects.get(id=self.kwargs['pk'])
        return context

    def form_valid(self, form, **kwargs):
        form.instance.car = Car.objects.get(id=self.kwargs['pk'])
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        row = self.request.GET.get('row')
        p = self.request.GET.get('p')
        q = self.request.GET.get('q')
        options = '?p=' + p + '&row=' + row
        options += '&q=' + q
        return reverse_lazy('car_detail') + options


class CarsListView(LoginRequiredMixin, ListView):
    model = Car
    template_name = 'cars/cars.html'
    context_object_name = 'cars'
    paginate_by = 10

    def get_queryset(self):
        if self.request.GET.get('q'):
            q = self.request.GET.get('q')
            make_results = self.model.objects.filter(
                user=self.request.user, make=q).order_by('-pk')
            model_results = self.model.objects.filter(
                user=self.request.user, model=q).order_by('-pk')
            if make_results.exists():
                return make_results
            elif model_results.exists():
                return model_results
            else:
                return self.model.objects.none()
        return self.model.objects.filter(user=self.request.user).order_by('-pk')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')
        return context


class UpdateCarView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Car
    fields = ['make', 'model', 'vrn', 'year']
    success_message = 'Car info has been updated'

    def get_success_url(self, **kwargs):
        row = self.request.GET.get('row')
        p = self.request.GET.get('p')
        q = self.request.GET.get('q')
        options = '?p=' + p + '&row=' + row
        options += '&q=' + q
        messages.success(self.request, self.success_message)
        return reverse_lazy('car_detail') + options

    def test_func(self):
        if self.get_object().user == self.request.user:
            return True
        return False


class DeleteCarView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Car
    success_url = '/'

    def test_func(self):
        if self.get_object().user == self.request.user:
            return True
        return False

    def delete(self, request, *args, **kwargs):
        success_message = f'Car {self.get_object()} has been deleted'
        messages.success(self.request, success_message)
        return super().delete(request, *args, **kwargs)


class RepairsListView(LoginRequiredMixin, ListView):
    model = Repair
    paginate_by = 10

    def __get_car(self):
        cars = Car.objects.filter(user=self.request.user).order_by('-pk')
        if self.request.GET.get('q'):
            q = self.request.GET.get('q')
            make_results = Car.objects.filter(
                user=self.request.user, make=q).order_by('-pk')
            model_results = Car.objects.filter(
                user=self.request.user, model=q).order_by('-pk')
            if make_results.exists():
                cars = make_results
            elif model_results.exists():
                cars = model_results

        id = int(self.request.GET.get('row')) - 1
        page = int(self.request.GET.get('p')) - 1
        id = id + page * 10
        return cars[id]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['car'] = self.__get_car()
        context['row'] = self.request.GET.get('row')
        context['p'] = self.request.GET.get('p')
        context['q'] = self.request.GET.get('q')
        return context

    def get_queryset(self, **kwargs):
        return self.model.objects.filter(car=self.__get_car()).order_by('-pk')

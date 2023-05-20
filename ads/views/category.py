import json

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView

from ads.models import Categories


@method_decorator(csrf_exempt, name="dispatch")
class CategoryListView(ListView):
    queryset = Categories.objects.order_by('name')

    def get(self, request, *args, **kwargs):
        all_categories = Categories.objects.all()
        return JsonResponse([cat.serialize() for cat in all_categories], safe=False)


class CategoryDetailView(DetailView):
    model = Categories

    def get(self, request, *args, **kwargs):


        return JsonResponse(self.get_object().serialize())


@method_decorator(csrf_exempt, name="dispatch")
class CategoryCreateView(CreateView):
    model = Categories
    fields = '__all__'

    def post(self, request, *args, **kwargs):

        data = json.loads(request.body)
        new_category = Categories.objects.create(**data)
        return JsonResponse(new_category.serialize())


@method_decorator(csrf_exempt, name="dispatch")
class CategoryUpdateView(UpdateView):
    model = Categories
    fields = '__all__'

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        data = json.loads(request.body)

        self.object.name = data.get('name')

        self.object.save()

        return JsonResponse(self.object.serialize())


@method_decorator(csrf_exempt, name="dispatch")
class CategoryDeleteView(DeleteView):
    model = Categories
    success_url = '/'

    def delete(self, request, *args, **kwargs):

        super().delete(request, *args, *kwargs)

        return JsonResponse({'status': 'ok'})
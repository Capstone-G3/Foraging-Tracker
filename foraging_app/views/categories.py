from django.views import View
from django.shortcuts import render, redirect
from foraging_app.models import Species

class CategoriesView(View):
    def get(self, request):
        query = request.GET.get('q')
        if query:
            categories = Species.objects.filter(category__icontains=query).values('category').distinct()
        else:
            categories = Species.objects.values('category').distinct()
        categories_with_images = []
        for category in categories:
            first_species = Species.objects.filter(category=category['category']).first()
            if first_species:
                categories_with_images.append({
                    'category': category['category'],
                    'first_species': first_species
                })
        return render(request, 'categories.html', {'categories': categories_with_images, 'query': query})

class CategoryDetailView(View):
    def get(self, request, category):
        species_list = Species.objects.filter(category=category)
        return render(request, 'category_detail.html', {'category': category, 'species_list': species_list})

    def post(self, request, category):
        # Handle POST requests if needed (e.g., submitting a form)
        return redirect('category_detail', category=category)

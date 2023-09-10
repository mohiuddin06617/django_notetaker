from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from notes.models import Note
from notes.forms import NoteForm
from django.urls import reverse_lazy

PER_PAGE_NOTE = 10  # TODO: Load from .env


class NoteListView(LoginRequiredMixin, ListView):
    model = Note
    template_name = 'notes/note_list.html'
    context_object_name = 'notes'
    paginate_by = PER_PAGE_NOTE
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = Note.objects.filter(author=self.request.user)
        search_query = self.request.GET.get('q')

        if search_query:
            queryset = queryset.filter(Q(title__icontains=search_query))

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = self.request.GET.get('page')
        paginator = Paginator(self.object_list, self.paginate_by)

        context['current_page'] = paginator.get_page(page)
        return context


class NoteDetailView(LoginRequiredMixin, DetailView):
    model = Note
    template_name = 'notes/note_detail.html'
    context_object_name = 'note'


class NoteCreateView(LoginRequiredMixin, CreateView):
    model = Note
    template_name = 'notes/note_create.html'
    form_class = NoteForm
    success_url = reverse_lazy('notes:note_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class NoteUpdateView(LoginRequiredMixin, UpdateView):
    model = Note
    template_name = 'notes/note_update.html'
    form_class = NoteForm
    success_url = reverse_lazy('notes:note_list')


class NoteDeleteView(LoginRequiredMixin, DeleteView):
    model = Note
    template_name = 'notes/note_list.html'
    success_url = reverse_lazy('notes:note_list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.soft_delete()
        return redirect(self.success_url)

from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import Topic, Entry
from .forms import TopicForm, EntryForm

# Create your views here.
def index(request):
	"""home page"""
	return render(request, 'blogs/index.html')

@login_required
def topics(request):
	"""shows all the topics"""
	topics = Topic.objects.filter(owner=request.user).order_by('date_added')
	context = {'topics': topics}
	return render(request, 'blogs/topics.html', context)

@login_required
def topic(request, topic_id):
	"""shows one single topic and its entries"""
	topic = Topic.objects.get(id=topic_id)
	# Make sure topic belongs to current user
	if topic.owner != request.user:
		raise Http404

	entries = topic.entry_set.order_by('-date_added')
	context = {'topic': topic, 'entries': entries}
	return render(request, 'blogs/topic.html', context)

@login_required
def new_topic(request):
	"""adds a new topic."""
	if request.method != 'POST':
		# no data submitted- create blank form
		form = TopicForm()
	else:
		# POST data submitted- process data
		form = TopicForm(request.POST)
		if form.is_valid():
			new_topic = form.save(commit=False)
			new_topic.owner = request.user
			new_topic.save()
			return HttpResponseRedirect(reverse('blogs:topics'))

	context = {'form': form}
	return render(request, 'blogs/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
	"""Adds new entry for a chosen topic"""
	topic = Topic.objects.get(id=topic_id)
	if topic.owner != request.user:
		raise Http404

	if request.method != 'POST':
		form = EntryForm()
	else:
		form = EntryForm(data=request.POST)
		if form.is_valid():
			new_entry = form.save(commit=False)
			new_entry.topic = topic
			new_entry.save()
			return HttpResponseRedirect(reverse('blogs:topic', args=[topic_id]))

	context = {'topic': topic, 'form': form}
	return render(request, 'blogs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
	"""edits an existing entry"""
	entry = Entry.objects.get(id=entry_id)
	topic = entry.topic
	if topic.owner != request.user:
		raise Http404

	if request.method != 'POST':
		# Initital request- prefill form with the current entry
		form = EntryForm(instance=entry)
	else:
		# POST data submitted, process data.
		form = EntryForm(instance=entry, data=request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('blogs:topic', args=[topic.id]))

	context = {'entry': entry, 'topic': topic, 'form': form}
	return render(request, 'blogs/edit_entry.html', context)




















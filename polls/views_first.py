from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.http import Http404
from django.template import loader


from .models import Question

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))


def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    template = loader.get_template('polls/detail.html')
    context = {
        'question': question,
        }
    return HttpResponse(template.render(context, request))


def results(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        #raise Http404("Question does not exist")
        latest_question_list = Question.objects.order_by('-pub_date')[:5]
        template = loader.get_template('polls/index.html')
        context = {
            'latest_question_list': latest_question_list,
            'error_message' : ("Question %s does not exist.\nPlease try one of the following questions:" % str(question_id)),
            }
        return HttpResponse(template.render(context, request))
    
    template = loader.get_template('polls/results.html')
    context = {
        'question': question,
        }
    return HttpResponse(template.render(context, request))


def vote(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        template = loader.get_template('polls/detail.html')
        context = {
            'question': question,
            'error_message': "You didn't select a choice.",
            }
        return HttpResponse(template.render(context, request))
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


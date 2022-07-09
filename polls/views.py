from audioop import reverse
from unittest import loader
from django.shortcuts import get_object_or_404, render
from .models import Choice, Question
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views import generic
from django.utils import timezone
## views fuction 들은 request를 인자로 갖는다.
## view function 들은 HttpResponse 객체를 반환하거나 Http404같은 예외를 반환해야한다.
## index함수에서 polls/index.html에 context, request가 넘어감
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {#데이터 없을 땐 다시 detail.html로, question, error_message 보여줌
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:   # 데이터 있는 경우 
        selected_choice.votes += 1      # 표 1 올려주고 
        selected_choice.save()          # 저장
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
                        # PoST 인 경우 HttpResponseRedirect

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})
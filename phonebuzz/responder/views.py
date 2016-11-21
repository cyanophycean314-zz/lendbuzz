from django.shortcuts import render, render_to_response
from django.template import RequestContext, Context
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import twilio.twiml
from twilio.util import RequestValidator

test_credentials = "58852d55d7fe7a083b60a081d9818ddd"
from django.http import HttpResponseForbidden

# Create your views here.
@csrf_exempt
def index(request):
	resp = twilio.twiml.Response()		
	validator = RequestValidator(test_credentials)
	if validator.validate(request.build_absolute_uri(), request.POST, request.META.get('HTTP_X_TWILIO_SIGNATURE',"fail")):
		print 'Yay for twilio'
	else:
		print 'Not twilio resopnse!'
		return HttpResponseForbidden()
	resp.say("Welcome to Kevin's PhoneBuzz! To play, please enter a number on the keypad and then press pound.")
	with resp.gather(finishOnKey='#',action = 'player', method='POST',timeout=10) as g:
		resp.redirect('')
	resp.redirect('player')
	return HttpResponse(str(resp))

@csrf_exempt
def player(request):
	digits = request.POST.get('Digits', ['*'])
	resp = twilio.twiml.Response()
	if '#' in digits or '*' in digits:
		resp.say("Error entering number")
		return HttpResponse(str(resp))
	num = int(''.join(digits))
	for i in range(1,num + 1):
		if i % 3 == 0:
			resp.say('Fizz')
		if i % 5 == 0:
			resp.say('Buzz')
		if i % 3 != 0 and i % 5 != 0:
			resp.say(str(i))
	resp.say('Wow that was so fun!')
	return HttpResponse(str(resp))
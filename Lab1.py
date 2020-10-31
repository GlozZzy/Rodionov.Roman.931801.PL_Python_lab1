from json import JSONDecodeError
from dateutil.tz import tzlocal
from pytz import timezone, UnknownTimeZoneError
import json
from datetime import datetime
from tzlocal import get_localzone


def app(environ, start_response):
    # Request is POST
    if environ['REQUEST_METHOD'] == 'POST':
        received_data = environ['wsgi.input'].read().decode("utf-8")

        # check received_data on json format
        try:
            received_data = json.loads(received_data)
        except JSONDecodeError:
            start_response('200 OK', [('Content-Type', 'text/plain')])
            return [b'Incorrect data. Use json.dumps()']

        # data processing
        try:
            type_ = received_data['type']
        except KeyError:
            start_response('200 OK', [('Content-Type', 'text/plain')])
            return [b'Not found argument "type"']

        try:
            tz1 = received_data['tz1']
        except KeyError:
            tz1 = None

        try:
            tz2 = received_data['tz2']
        except KeyError:
            tz2 = None

        if tz1:
            try:
                tz1 = timezone(tz1)
            except UnknownTimeZoneError:
                start_response('200 OK', [('Content-Type', 'text/plain')])
                return [b'Unknown time zone tz1']

        if tz2:
            try:
                tz2 = timezone(tz2)
            except UnknownTimeZoneError:
                start_response('200 OK', [('Content-Type', 'text/plain')])
                return [b'Unknown time zone tz2']

        if type_ == 'date':
            answer = json.dumps({'date': datetime.now(tz=tz1).date().isoformat(), 'tz': str(tz1)})
        elif type_ == 'time':
            answer = json.dumps({'time': datetime.now(tz=tz1).time().isoformat(), 'tz': str(tz1)})
        elif type_ == 'datediff':
            try:
                d1 = datetime.now(tz=tz1).tzinfo.localize(datetime.now())
            except:
                d1 = datetime.now(tzlocal())
                tz1 = get_localzone()
            try:
                d2 = datetime.now(tz=tz2).tzinfo.localize(datetime.now())
            except:
                d2 = datetime.now(tzlocal())
                tz2 = get_localzone()

            result_diff = ''
            if d1 > d2:
                result_diff += '-' + str(d1 - d2)
            else:
                result_diff += str(d2 - d1)
            answer = json.dumps({'diff': result_diff, 'tz1': str(tz1), 'tz2': str(tz2)})

        else:
            start_response('200 OK', [('Content-Type', 'text/plain')])
            return [b'Incorrect type (should: "time" or "date" or "datediff")']

        start_response('200 OK', [('Content-Type', 'text/plain')])
        return [bytes(answer, encoding='utf-8')]

    # Request is GET
    else:
        input_timezone = environ['PATH_INFO'][1:]
        if input_timezone:
            try:
                input_timezone = timezone(input_timezone)
            except UnknownTimeZoneError:
                start_response('200 OK', [('Content-Type', 'text/plain')])
                return [b'Unknown time zone']
        else:
            input_timezone = None

        string = 'Time '
        if input_timezone is None:
            string += 'on server:\n'
        else:
            string += 'in %s:\n' % input_timezone

        start_response('200 OK', [('Content-Type', 'text/plain')])
        return [bytes(string + datetime.now(tz=input_timezone).time().isoformat() + '\nAdd needed timezone to the url\n'
                      , encoding='utf-8')]


if __name__ == '__main__':
    from paste import reloader
    from paste.httpserver import serve

    reloader.install()
    serve(app)
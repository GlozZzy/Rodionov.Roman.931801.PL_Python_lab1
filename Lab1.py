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
            tz_start = received_data['tz_start']
        except KeyError:
            tz_start = None

        try:
            tz_end = received_data['tz_end']
        except KeyError:
            tz_end = None

        if tz_start:
            try:
                tz_start = timezone(tz_start)
            except UnknownTimeZoneError:
                start_response('200 OK', [('Content-Type', 'text/plain')])
                return [b'Unknown time zone tz_start']
        else:
            tz_start = get_localzone()

        if tz_end:
            try:
                tz_end = timezone(tz_end)
            except UnknownTimeZoneError:
                start_response('200 OK', [('Content-Type', 'text/plain')])
                return [b'Unknown time zone tz_end']
        else:
            tz_end = get_localzone()

        if type_ == 'date':
            answer = json.dumps({'date': datetime.now(tz=tz_start).date().isoformat(), 'tz': str(tz_start)})
        elif type_ == 'time':
            answer = json.dumps({'time': datetime.now(tz=tz_start).time().isoformat(), 'tz': str(tz_start)})
        elif type_ == 'datediff':
            d_start = datetime.now(tz=tz_start).tzinfo.localize(datetime.now())
            d_end = datetime.now(tz=tz_end).tzinfo.localize(datetime.now())

            result_diff = ''
            if d_end > d_start:
                result_diff += '-' + str(d_end - d_start)
            else:
                result_diff += str(d_start - d_end)
            answer = json.dumps({'diff': result_diff, 'tz_start': str(tz_start), 'tz_end': str(tz_end)})

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

        msg = 'Time '
        if input_timezone:
            msg += 'in %s:\n' % input_timezone
        else:
            msg += 'on server:\n'

        start_response('200 OK', [('Content-Type', 'text/plain')])
        return [bytes(msg + datetime.now(tz=input_timezone).time().isoformat() + '\nAdd needed timezone to the url\n'
                      , encoding='utf-8')]


if __name__ == '__main__':
    from paste import reloader
    from paste.httpserver import serve

    reloader.install()
    serve(app)

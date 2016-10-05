from datetime import timedelta

from django.core.management import BaseCommand, CommandError

from timers.models import Timer


class Command(BaseCommand):
    help = (
        'Change a timer\'s nth interval start/end time by the given number '
        'of minutes.'
        'Usage:\n'
        '  ./manage.py change_interval <timer> <n> (start|end) (+|-) <minutes>'
    )

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument(
            'timer',
            help='The name of the timer whose nth interval should be changed.',
        )
        parser.add_argument(
            'n',
            type=int,
            help='The nth most recent interval to adjust; 0 = most recent.',
        )
        parser.add_argument(
            'start_or_end',
            choices=('start', 'end'),
            help='Whether to adjust the start or end of the interval.',
        )
        parser.add_argument(
            'plus_or_minus',
            choices=('+', '-'),
            help='Whether to adjust the interval forward or backward.',
        )
        parser.add_argument(
            'delta',
            type=int,
            help='Number of minutes to add or subtract.',
        )

    def handle(self, **options):
        timer_name = options['timer']
        n = int(options['n'])

        s_or_e = options['start_or_end']
        adjust_start = s_or_e == 'start'

        p_or_m = options['plus_or_minus']
        later = p_or_m == '+'
        back_or_forward = 'forward' if p_or_m == '+' else 'back'

        delta = int(options['delta'])

        try:
            timer = Timer.objects.get(name=timer_name)
        except Timer.DoesNotExist:
            raise CommandError(
                'Could not find a Timer name "{0}".'
                .format(timer_name)
            )
        except Timer.MultipleObjectsReturned:
            raise CommandError(
                'Found multiple timers named "{0}"... sorry!'
                .format(timer_name)
            )

        try:
            interval = timer.interval_set.all()[n]
        except IndexError:
            raise CommandError('Could not find the requested interval.')

        self.stdout.write(
            'Would adjust the "{timer}" interval[{n}] '
            '{start_or_end} time {back_or_forward} by {delta} minutes.'
            .format(
                timer=timer_name,
                n=n,
                start_or_end=s_or_e,
                back_or_forward=back_or_forward,
                delta=delta,
            )
        )

        self.stdout.write(
            'Current interval timespan...\n'
            '   start: {0}\n'
            '     end: {1}\n'
            '  length: {2}\n'
            .format(interval.start, interval.end, interval.length)
        )

        diff = timedelta(minutes=delta)
        if adjust_start:
            if later:
                interval.start += diff
            else:
                interval.start -= diff
        else:
            if later:
                interval.end += diff
            else:
                interval.end -= diff

        self.stdout.write(
            'New interval timespan...\n'
            '   start: {0}\n'
            '     end: {1}\n'
            '  length: {2}'
            .format(interval.start, interval.end, interval.length)
        )

        confirm = input('Save this change (y/n)? ')
        if confirm == 'y':
            interval.save()

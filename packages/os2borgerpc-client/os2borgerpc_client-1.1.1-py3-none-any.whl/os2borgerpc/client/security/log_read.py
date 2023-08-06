from datetime import date, datetime, timedelta
# Search syslog from the end to a certain time
# Syslog is by Ubuntu default rotated daily


def read(sec, fname):
    data = ""
    year = date.today().year

    with open(fname) as f:
        for line in reversed(f.readlines()):
            line = str(line.replace('\0', ''))
            date_object = datetime.strptime(str(year) + ' ' + line[:15],
                                            '%Y %b  %d %H:%M:%S')
            # Detect lines from within the last x seconds
            if (datetime.now() - timedelta(seconds=sec)) <= date_object:
                data = line + data

    return data

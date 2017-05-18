


def is_redirect_rule(line):
    words = line.split()
    if len(words) < 1:
        return False

    if words[0] != 'Redirect':
        return False

    return True


def is_410_redirect(line):
    words = line.split()
    if words[1] == 'Gone':
        return True
    return False


def get_status_code(line):
    if is_410_redirect(line):
        return "410"
    words = line.split()
    return words[1]


def get_route(line):
    words = line.split()
    return words[2]


def get_destination(line):
    if is_410_redirect(line):
        return ""
    words = line.split()
    return words[3]


#######################################################
lines = [line.rstrip('\n') for line in open('htaccess')]
routes = []

for line in lines:
    if is_redirect_rule(line):
        status_code = get_status_code(line)
        route = get_route(line)
        str_redirect = """
location {} {{
    rewrite ^(.*)$  {} permanent;
}} """
        str_gone = """
location {} {{
    return 410;
}}"""

        if route not in routes:
            if status_code == "301":
                print('\t' + str_redirect.format(route, get_destination(line), "permanent"))
            elif status_code == "410":
                print('\t' + str_gone.format(route, get_destination(line)))
            else:
                raise Exception("Unknown status code " + status_code)

        routes.append(route)

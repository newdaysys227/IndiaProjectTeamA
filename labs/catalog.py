# -*- coding: utf-8 -*-
"""
Lab catalog (metadata and code difference).
The index / detail templates read this and show it.

Each lab has a working demo for "before" (vulnerable) and "after" (secure).
All on-screen text uses simple English.
"""

LABS = [
    {
        "slug": "sql-injection",
        "no": 1,
        "category": "SQL Injection",
        "title": "SQL Injection in Search",
        "difficulty": "Easy",
        "summary": (
            "The search box puts your text straight into the SQL. "
            "So you can add SQL words and see hidden items that should not show."
        ),
        "goal": "Make a hidden item (not for sale) show in the results.",
        "try_hint": "Type   ' OR 1=1 --   in the search box.",
        "fix": (
            "Do not glue user text into SQL. Send it as a value (use a placeholder). "
            "Use the ORM when you can."
        ),
        "code_before": '''# Before: it glues text into the SQL (not safe)
def search(request):
    keyword = request.GET.get("q", "")
    sql = (
        "SELECT name, category, price FROM labs_product "
        "WHERE released = 1 AND name LIKE '%" + keyword + "%'"
    )
    with connection.cursor() as cur:
        cur.execute(sql)        # <- keyword can add SQL words
        rows = cur.fetchall()
''',
        "code_after": '''# After: it sends the value safely with a placeholder
def search(request):
    keyword = request.GET.get("q", "")
    sql = (
        "SELECT name, category, price FROM labs_product "
        "WHERE released = 1 AND name LIKE %s"
    )
    with connection.cursor() as cur:
        cur.execute(sql, ["%" + keyword + "%"])   # <- value is not read as SQL
        rows = cur.fetchall()
''',
    },
    {
        "slug": "xss-reflected",
        "no": 2,
        "category": "Cross-Site Scripting (XSS)",
        "title": "Reflected XSS",
        "difficulty": "Easy",
        "summary": (
            "The search word is put back into the page with no cleaning. "
            "So a <script> in your text runs in the browser."
        ),
        "goal": "Make JavaScript run on the result page.",
        "try_hint": "Type   <script>alert(1)</script>   in the search box.",
        "fix": (
            "Always clean (escape) text before you show it. "
            "Let Django auto-escape. Do not add |safe."
        ),
        "code_before": '''# Before: it puts text into HTML with no cleaning
def reflected(request):
    q = request.GET.get("q", "")
    html = f"<p>No results for '{q}'.</p>"
    return HttpResponse(html)   # <- q is read as HTML
''',
        "code_after": '''# After: it cleans (escapes) the text first
from django.utils.html import escape

def reflected(request):
    q = request.GET.get("q", "")
    html = f"<p>No results for '{escape(q)}'.</p>"
    return HttpResponse(html)   # <- <script> is shown as text only
''',
    },
    {
        "slug": "xss-stored",
        "no": 3,
        "category": "Cross-Site Scripting (XSS)",
        "title": "Stored XSS",
        "difficulty": "Medium",
        "summary": (
            "A comment is saved and shown with no cleaning. "
            "A bad comment runs in the browser of everyone who opens the page."
        ),
        "goal": "Post a comment with a script. It runs for people who open the page.",
        "try_hint": "Post   <script>alert(document.cookie)</script>   as a comment.",
        "fix": (
            "Saving is OK. But clean (escape) when you show it. "
            "Remove |safe and let auto-escape work."
        ),
        "code_before": '''{# Before: |safe turns off auto-escape #}
{% for c in comments %}
  <div class="comment">
    <b>{{ c.author }}</b>: {{ c.body|safe }}   {# <- safe is the danger #}
  </div>
{% endfor %}
''',
        "code_after": '''{# After: let auto-escape do the work #}
{% for c in comments %}
  <div class="comment">
    <b>{{ c.author }}</b>: {{ c.body }}         {# <- <script> becomes text #}
  </div>
{% endfor %}
''',
    },
    {
        "slug": "csrf",
        "no": 4,
        "category": "CSRF",
        "title": "CSRF on Change Email",
        "difficulty": "Medium",
        "summary": (
            "The change-email form has no CSRF check (@csrf_exempt). "
            "A trap page can change the email of a logged-in user."
        ),
        "goal": "Change the email of a logged-in user from a trap page on another site.",
        "try_hint": 'Click "Open trap page" to see the attack.',
        "fix": (
            "Remove @csrf_exempt. Use the CSRF check and "
            "{% csrf_token %} in the form."
        ),
        "code_before": '''# Before: the CSRF check is turned off
@csrf_exempt
def change_email(request):
    if request.method == "POST":
        new_email = request.POST.get("email")
        request.session["email"] = new_email   # <- change with no token check
    ...
''',
        "code_after": '''# After: keep the CSRF check on (no @csrf_exempt)
def change_email(request):
    if request.method == "POST":
        new_email = request.POST.get("email")
        request.session["email"] = new_email   # <- no good token -> blocked
    ...
# The <form> must have {% csrf_token %}
''',
    },
    {
        "slug": "auth",
        "no": 5,
        "category": "Authentication",
        "title": "Username Enumeration and Brute Force",
        "difficulty": "Medium",
        "summary": (
            "The login shows a different message for 'no such user' and "
            "'wrong password'. So you can find real user names. "
            "There is no try limit, so you can guess many times."
        ),
        "goal": "Find a real user name from the different messages.",
        "try_hint": "Try a real user (admin) and a fake user (nobody). Look at the different messages.",
        "fix": (
            "Use the same message for all fails. Do not show if the user name exists. "
            "Also add a limit on tries (lock)."
        ),
        "code_before": '''# Before: the message changes by reason + no try limit
def login_view(request):
    u = User.objects.filter(username=username).first()
    if u is None:
        msg = "No such user name"          # <- tells if the user exists
    elif not u.check_password(password):
        msg = "Wrong password"             # <- you can tell them apart
    else:
        msg = "Login OK"
''',
        "code_after": '''# After: same message + limit the tries
def login_view(request):
    if attempts_exceeded(request):          # <- lock after some tries
        msg = "Too many tries. Please wait."
    else:
        user = authenticate(username=username, password=password)
        msg = "Login OK" if user else "Wrong user name or password"
        # ^ same message, you cannot tell them apart
''',
    },
    {
        "slug": "path-traversal",
        "no": 6,
        "category": "Path Traversal",
        "title": "Path Traversal in File View",
        "difficulty": "Easy",
        "summary": (
            "The file name is glued to the path with no check. "
            "So you can use ../ to read files outside the open folder."
        ),
        "goal": "Read secret.txt that is outside the open folder.",
        "try_hint": "Type   ../secret.txt   as the file name.",
        "fix": (
            "Remove the folder part of the name (basename). "
            "Then check the full path stays inside the open folder."
        ),
        "code_before": '''# Before: it glues the name as is
def view_file(request):
    name = request.GET.get("name", "")
    path = os.path.join(PUBLIC_DIR, name)   # <- ../ can go outside
    with open(path, encoding="utf-8") as f:
        return HttpResponse(f.read(), content_type="text/plain")
''',
        "code_after": '''# After: basename removes folders, then check it stays inside
def view_file(request):
    name = os.path.basename(request.GET.get("name", ""))   # <- remove ../
    path = os.path.realpath(os.path.join(PUBLIC_DIR, name))
    if not path.startswith(os.path.realpath(PUBLIC_DIR) + os.sep):
        return HttpResponseBadRequest("Bad file name")
    with open(path, encoding="utf-8") as f:
        return HttpResponse(f.read(), content_type="text/plain")
''',
    },
    {
        "slug": "os-command",
        "no": 7,
        "category": "OS Command Injection",
        "title": "OS Command Injection in Ping",
        "difficulty": "Medium",
        "summary": (
            "The host name is glued into a shell command. So ; or && can run "
            "another command too. "
            "(This demo does not run real OS commands. It only shows what would happen.)"
        ),
        "goal": "Run another command from the host name box.",
        "try_hint": "Type   127.0.0.1; whoami   as the host name.",
        "fix": (
            "Do not use shell=True and string glue. Pass args as a list. "
            "Allow only host-name letters."
        ),
        "code_before": '''# Before: shell=True + string glue (not safe)
def ping(request):
    host = request.GET.get("host", "")
    cmd = "ping -n 1 " + host                 # <- host can add ; whoami
    out = subprocess.check_output(cmd, shell=True, text=True)
    return HttpResponse(out)
''',
        "code_after": '''# After: pass args as a list and check the input
import re
def ping(request):
    host = request.GET.get("host", "")
    if not re.fullmatch(r"[A-Za-z0-9.\\-]+", host):   # <- only safe letters
        return HttpResponseBadRequest("Bad host name")
    out = subprocess.check_output(
        ["ping", "-n", "1", host], shell=False, text=True
    )                                                  # <- no shell
    return HttpResponse(out)
''',
    },
    {
        "slug": "idor",
        "no": 8,
        "category": "Broken Access Control",
        "title": "IDOR (See Another User's Account)",
        "difficulty": "Easy",
        "summary": (
            "The account page uses only the id in the URL. "
            "It does not check who owns it. "
            "Change the id and you can see other people's accounts."
        ),
        "goal": "Open an account id that is not yours and see it.",
        "try_hint": "Change ?id= to 1, 2, 3 ... and see other accounts.",
        "fix": (
            "When you get the data, always check the logged-in user is the owner."
        ),
        "code_before": '''# Before: get by id only (no owner check)
@login_required
def account(request):
    account_id = request.GET.get("id")
    acc = Account.objects.get(pk=account_id)   # <- any id works
    return render(request, "...", {"acc": acc})
''',
        "code_after": '''# After: get only if the user is the owner
@login_required
def account(request):
    account_id = request.GET.get("id")
    acc = get_object_or_404(
        Account, pk=account_id, owner=request.user   # <- only my account
    )
    return render(request, "...", {"acc": acc})
''',
    },
    {
        "slug": "file-upload",
        "no": 9,
        "category": "File Upload",
        "title": "Upload With No File-Type Check",
        "difficulty": "Medium",
        "summary": (
            "Files are saved to the open folder with no check. "
            "An HTML or script file can run in the browser of a visitor."
        ),
        "goal": "Upload an HTML file. See that it is served and runs.",
        "try_hint": "Upload a .html file with <script>alert(1)</script> inside. (The safe one blocks it.)",
        "fix": (
            "Allow only some file types (a list). Make the file name safe and random "
            "on the server. If you can, save where it cannot run, and send it as a download."
        ),
        "code_before": '''# Before: take any file and keep the real name
def upload(request):
    f = request.FILES["file"]
    path = os.path.join(MEDIA_ROOT, f.name)   # <- same name and type
    with open(path, "wb") as out:
        for chunk in f.chunks():
            out.write(chunk)
''',
        "code_after": '''# After: allow only some types and use a random name
import uuid
ALLOWED = {".png", ".jpg", ".jpeg", ".gif", ".txt"}
def upload(request):
    f = request.FILES["file"]
    ext = os.path.splitext(f.name)[1].lower()
    if ext not in ALLOWED:                    # <- block .html/.js
        return HttpResponseBadRequest("File type not allowed")
    safe_name = uuid.uuid4().hex + ext        # <- name is hard to guess
    path = os.path.join(MEDIA_ROOT, safe_name)
    with open(path, "wb") as out:
        for chunk in f.chunks():
            out.write(chunk)
''',
    },
]

LABS_BY_SLUG = {lab["slug"]: lab for lab in LABS}

import webbrowser
def webpage(format):
  html_template=format
  with open('frame.html', "w", encoding="utf-8") as f:
      f.write(html_template)
  webbrowser.open('frame.html')
  f.close()
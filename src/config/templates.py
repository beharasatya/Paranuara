tpl_start = '''<html>
  <head>
      <title>Paranura</title>
	  <link rel="stylesheet" href="/styles.css">	  
  </head>
  <body>'''

tpl_form_cmp = '''
    <form method="post" action="/search/company" align="center">
        
        <fieldset align="center">
        <legend align="center">Company Search</legend> <br>
			<br/>
			<b>Enter Company's Name</b> <br><input id="textboxid" name='company' required>
			<br/><br/>
			<input id="searchbox" type='submit' value='Search'>
        </fieldset>
        <p>
		    <pre>
		        <code style=display:block;white-space:pre-wrap>
		        {res_tag}
		        </code>
		    </pre>
		</p>
    </form>'''


tpl_br = '''<br/> <br/>'''
    
tpl_form_ppl = '''
    <form method="post" action="/search/people" align="center">
        
        <fieldset align="center">
        <legend align="center">People Search</legend> <br>
			<br/>
			<b>Enter People's Name</b> <br><input id="textboxid" name='p1' required>
			<br/><br/>
			<b>Enter People's Name</b> <br><input id="textboxid" name='p2'>
			<br/><br/>
			<input id="searchbox" type='submit' value='Search'>
			<br/> <br/>
		</fieldset>
		<p>
		    <pre>
		        <code style=display:block;white-space:pre-wrap>
		        {res_tag}
		        </code>
		    </pre>
		</p>
    </form>'''


p_tag = '''<p><pre><code style=display:block;white-space:pre-wrap>{txt}</pre></p>'''


auth_tag = '''<p>By <i>{author}</i></p>'''

title_tag = '''<p><a href='{url}' target="_blank"><b>{title}</b></a></p>'''

tpl_end = '''</body>
         </html> '''

tpl_home = tpl_start + tpl_form_cmp.format(res_tag='') + tpl_br + tpl_form_ppl.format(res_tag='') + tpl_end
tpl_404 = '''
        <h1>404</h1>
        <h2>Oops! Page Not Found</h2>
        <p>Sorry, but you are looking for something that isn't here.</p> '''

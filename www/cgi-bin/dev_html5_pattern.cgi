#!/bin/sh

# Version: 7.0.0 2020-05-17

# Title: HTML5 Pattern Test
# Description: Used for testing HTML regex pattern matching

. pcp-functions

pcp_html_head "HTML5 Pattern Test Page" "PH"

pcp_navbar
pcp_httpd_query_string_no_decode

#========================================================================================
pcp_heading5 "HTML5 Pattern Test"
#----------------------------------------------------------------------------------------
echo '    <div class="row">'
echo '      <form name="LMS" action="'$0'">'
echo '        <div class="row">'
echo '          <div class="col-6">'
echo '            <p>Submit</p>'
echo '          </div>'
echo '          <div class="col">'
echo '            <p>Enter HTML5 Pattern Here.</p>'
echo '          </div>'
echo '          <div class="col-6">'
echo '            <p>Type test strings here.</p>'
echo '          </div>'
echo '        </div>'
echo '        <div class="row">'
echo '          <div class="col-4">'
echo '            <button type="submit" name="ACTION" value="Submit">Submit</button>'
echo '          </div>'
echo '          <div class="col-4">'
echo '            <input id="PATTERN" class="XXXX" type="text" name="PATTERN" onchange="setpattern()">'
echo '          </div>'
echo '          <div class="col-4">'
echo '            <input id="TEST" class="XXXX" type="text" name="TEST" required pattern="" onclick="setpattern()">'
echo '          </div>'
echo '        </div>'
echo '      </form>'
echo '      <div class="row">'
echo '        <div class="col-5">'
echo '          <p>CGI Pattern Code</p>'
echo '        </div>'
echo '        <div class="col-6">'
echo '          <p id="OUT">Enter HTML5 Pattern Here.</p>'
echo '        </div>'
echo '      </div>'
echo '    </div>'

echo '<script>'
echo '  var Box = "PATTERN";'
echo '  var Box1 = "TEST";'
echo '  var pattern = "'${PATTERN}'";'
echo '  var test = "'${TEST}'";'
echo '  document.getElementById(Box).value = decodeURIComponent(pattern.replace(/\+/g, "%20"));'
echo '  document.getElementById(Box1).value = decodeURIComponent(test.replace(/\+/g, "%20"));'
echo '  function setpattern() {'
echo '    document.getElementById(Box1).pattern = document.getElementById(Box).value;'
echo '  }'
echo '  function setout() {'
echo '    var tmp = "pattern=\"" + decodeURIComponent(pattern.replace(/\+/g, "%20")) + "\"";'
echo '    document.getElementById("OUT").innerHTML = tmp.replace(/\\/g, "\\\\");'
echo '  }'
echo '  setpattern();'
echo '  setout();'
echo '</script>'

pcp_html_end
exit

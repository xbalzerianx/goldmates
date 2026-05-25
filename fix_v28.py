import os

with open('/tmp/cairspa_v27.js') as f:
    js = f.read()

token = os.environ.get('BASE44_SERVICE_TOKEN', '')
app_id = '69b7cae883aa8d618e49d211'

old_submit = 'c=async d=>{d.preventDefault();const btn=d.target.querySelector("button[type=submit]");btn.disabled=!0;btn.textContent="Sending...";try{const res=await fetch("https://api.base44.com/api/apps/69b7cae883aa8d618e49d211/functions/submitForm",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({type:"lead",name:u.name,email:u.email,phone:u.phone,service:u.service,message:u.message,form_type:"Hero Callback"})});if(res.ok){f({name:"",email:"",phone:"",service:"",message:""});btn.textContent="\u2713 Sent! We\'ll be in touch.";btn.style.background="#2D7D46";}else{btn.disabled=!1;btn.textContent="REQUEST A CALLBACK";alert("Something went wrong. Please try again.");}}catch(e){btn.disabled=!1;btn.textContent="REQUEST A CALLBACK";alert("Something went wrong. Please try again.");}};'

# Build new submit as plain string
new_submit = (
    'c=async d=>{'
    'd.preventDefault();'
    'const btn=d.target.querySelector("button[type=submit]");'
    'btn.disabled=!0;btn.textContent="Sending...";'
    'try{'
    'const res=await fetch("https://base44.app/api/apps/' + app_id + '/entities/LeadForm",{'
    'method:"POST",'
    'headers:{"Content-Type":"application/json","Authorization":"Bearer ' + token + '"},'
    'body:JSON.stringify({name:u.name,email:u.email,phone:u.phone,service_interest:u.service,message:u.message,form_type:"Hero Callback",status:"New"})'
    '});'
    'if(res.ok){'
    'f({name:"",email:"",phone:"",service:"",message:""});'
    'const overlay=document.createElement("div");'
    'overlay.id="cair-thankyou-overlay";'
    'overlay.style.cssText="position:fixed;inset:0;background:rgba(0,0,0,0.6);z-index:99999;display:flex;align-items:center;justify-content:center;";'
    'const box=document.createElement("div");'
    'box.style.cssText="background:#fff;border-radius:20px;padding:44px 36px 36px;max-width:440px;width:90%;text-align:center;box-shadow:0 24px 80px rgba(0,0,0,0.3);";'
    'box.innerHTML="<div style=\'font-size:56px;margin-bottom:14px\'>\uD83C\uDF38</div>"'
    '+"<h3 style=\'font-family:Georgia,serif;font-size:24px;color:#2D2926;margin:0 0 12px\'>Thank You!</h3>"'
    '+"<p style=\'font-family:Arial,sans-serif;color:#6B5E52;font-size:15px;line-height:1.7;margin:0 0 20px\'>"'
    '+"We received your consultation request and our team will be in touch shortly.</p>"'
    '+"<p style=\'font-family:Arial,sans-serif;color:#6B5E52;font-size:14px;margin:0 0 8px\'>Need to speak with us now?</p>"'
    '+"<a href=\'tel:+17143322838\' style=\'display:inline-block;font-size:22px;font-weight:700;color:#b84342;text-decoration:none;margin-bottom:28px\'>\uD83D\uDCDE (714) 332-2838</a><br>"'
    '+"<button id=\'cair-close-ty\' style=\'background:#b84342;color:#fff;border:none;padding:13px 36px;border-radius:8px;font-family:Arial,sans-serif;font-size:13px;font-weight:700;letter-spacing:1.5px;cursor:pointer;text-transform:uppercase\'>Close</button>";'
    'overlay.appendChild(box);'
    'overlay.addEventListener("click",e=>{if(e.target===overlay)overlay.remove()});'
    'document.body.appendChild(overlay);'
    'document.getElementById("cair-close-ty").addEventListener("click",()=>overlay.remove());'
    'btn.disabled=!1;btn.textContent="REQUEST A CALLBACK";'
    '}else{'
    'const errText=await res.text();console.error("Submit error:",errText);'
    'btn.disabled=!1;btn.textContent="REQUEST A CALLBACK";'
    'alert("Something went wrong. Please try again.");'
    '}'
    '}catch(e){'
    'console.error("Submit exception:",e);'
    'btn.disabled=!1;btn.textContent="REQUEST A CALLBACK";'
    'alert("Something went wrong. Please try again.");'
    '}};'
)

if old_submit in js:
    js = js.replace(old_submit, new_submit, 1)
    print("SUCCESS: Fixed fetch URL + added thank-you modal with phone number")
else:
    print("NOT FOUND — searching nearby...")
    idx = js.find('api.base44.com')
    if idx != -1:
        print(repr(js[idx-300:idx+500]))
    else:
        idx2 = js.find('btn.textContent="Sending')
        print(f"Sending... at {idx2}")
        print(repr(js[idx2-300:idx2+500]))

with open('/tmp/cairspa_v28.js', 'w') as f:
    f.write(js)
print(f"Saved v28.js — {len(js)} chars")

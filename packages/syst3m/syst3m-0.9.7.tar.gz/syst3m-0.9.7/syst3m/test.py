#!/usr/bin/env python3
import os,sys,time,random
sys.path.insert(1, ".")
import syst3m


browser = syst3m.browser.Browser()

# login.
browser.get("https://waves.com/login")

# already signed in.
#signed_in = browser.get_element(element="p", attribute="class", value="bold align-center margin-top-25")

# send keys.
username = browser.get_element(element="input", attribute="id", value="username-tb")
password = browser.get_element(element="input", attribute="id", value="cart-2-returning-password")
enter = browser.get_element(element="input", attribute="title", value="Continue")
username.send_keys("dbergh4444@gmail.com")
time.sleep(random.randrange(8, 16)/10)
password.send_keys("Doeman12!")
time.sleep(random.randrange(8, 16)/10)
enter.click()
time.sleep(random.randrange(8, 16)/10)
print(">>> Finish the login")
success = False
for i in range(10000000):
	if "waves.com/login" not in browser.driver.current_url: 
		success = True
		break
	time.sleep(1)
print("LOGGED IN")

# install demos.
demos = [
	"https://www.waves.com/account/demo-complete?demo=/plugins/cla-drums",
	"https://www.waves.com/demo?demo=/plugins/z-noise",
	"https://www.waves.com/demo?demo=/plugins/cla-76-compressor-limiter",
	"https://www.waves.com/demo?demo=/plugins/oneknob-filter",
	"https://www.waves.com/demo?demo=/plugins/trueverb",
	"https://www.waves.com/demo?demo=/plugins/h-delay-hybrid-delay",
	"https://www.waves.com/demo?demo=/plugins/s1-stereo-imager",
	"https://www.waves.com/demo?demo=/plugins/puigtec-eqs",
	"https://www.waves.com/demo?demo=/plugins/renaissance-vox",
	"https://www.waves.com/demo?demo=/plugins/infected-mushroom-pusher",
	"https://www.waves.com/demo?demo=/plugins/cla-vocals",
	"https://www.waves.com/demo?demo=/plugins/cla-guitars",
	"https://www.waves.com/demo?demo=/plugins/cla-bass",
	"https://www.waves.com/demo?demo=/plugins/cla-effects",
	"https://www.waves.com/demo?demo=/plugins/cla-mixdown",
	"https://www.waves.com/demo?demo=/plugins/l1-ultramaximizer",
	"https://www.waves.com/demo?demo=/plugins/deesser",
	"https://www.waves.com/demo?demo=/plugins/l2-ultramaximizer",
	"https://www.waves.com/demo?demo=/plugins/soundshifter",
	"https://www.waves.com/demo?demo=/plugins/debreath",
	"https://www.waves.com/demo?demo=/plugins/doubler",
	"https://www.waves.com/demo?demo=/plugins/ssl-e-channel",
	"https://www.waves.com/demo?demo=/plugins/v-eq4",
	"https://www.waves.com/demo?demo=/plugins/cla-2a-compressor-limiter",
	"https://www.waves.com/demo?demo=/plugins/cla-3a-compressor-limiter",
	"https://www.waves.com/demo?demo=/plugins/vocal-rider",
	"https://www.waves.com/demo?demo=/plugins/c6-multiband-compressor",
	"https://www.waves.com/demo?demo=/plugins/ns1-noise-suppressor",
	"https://www.waves.com/demo?demo=/plugins/oneknob-driver",
	"https://www.waves.com/demo?demo=/plugins/oneknob-brighter",
	"https://www.waves.com/demo?demo=/plugins/metafilter",
	"https://www.waves.com/demo?demo=/plugins/h-reverb-hybrid-reverb",
	"https://www.waves.com/demo?demo=/plugins/f6-floating-band-dynamic-eq",
]
for url in demos:
	print(url)
	browser.get(url)
	success = False
	for i in range(120):
		try:
			e = browser.get_element(element="p", attribute="class", value="ok-box").text
			if "Your demo was successfully registered in your account." in e or "You have already demoed this product or a bundle containing this product." in e:
				success = True
				break
		except: a=1
		try:
			e = browser.get_element(element="p", attribute="class", value="error-box").text
			if "You have already demoed this product or a bundle containing this product." in e:
				success = True
				break
		except: a=1
		time.sleep(1)
	if not success: raise ValueError(f"Failed to activate demo {url}.")
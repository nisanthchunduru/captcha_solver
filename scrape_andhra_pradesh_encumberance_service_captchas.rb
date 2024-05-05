# Scrape captchas from Andhra Pradesh Encumberance Service

require "uri"
require "net/http"

url = URI("https://rs.ap.gov.in/APCARDECClient/FetchHelpDetails")

https = Net::HTTP.new(url.host, url.port)
https.use_ssl = true

request = Net::HTTP::Post.new(url)
request["sec-ch-ua"] = "\"Brave\";v=\"119\", \"Chromium\";v=\"119\", \"Not?A_Brand\";v=\"24\""
request["sec-ch-ua-mobile"] = "?0"
request["sec-ch-ua-platform"] = "\"macOS\""
request["Upgrade-Insecure-Requests"] = "1"
request["Content-Type"] = "application/x-www-form-urlencoded"
request["User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
request["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8"
request["Sec-GPC"] = "1"
request["host"] = "rs.ap.gov.in"
request["Cookie"] = "JSESSIONID=2NJrlrvPWfK75Znn7n6H8xylvVd7kJCgTyXVQvBpnwJDwp0Mvv9t!1163408210"
request.body = "apt=&block=&captcha=54067&colony=&distcode=&distname=&districtCode=3&districtName=&docSel=1&doct=1500&east=&endDate=&fno=&hlpdocyear=&hno=&houseno2=&houseno3=&houseno4=&jurisdiction=&newdistrictCode=03&north=&path=%2FAPCARDECClient&pno=&regDate=&regyear=2021&scheduleno=&selectedSroId=null&south=&sro=&sroId=314&sroList=&sroName=&sroVal=DWARAKANAGAR%20(314)&srocode=&sroname=&startDate=&surveyno2=&surveyno3=&surveyno4=&syno=&vill1=&vill1a=&vill2=&vill2a=&village=&villagecode=&west=&word="

response = https.request(request)
puts response.read_body

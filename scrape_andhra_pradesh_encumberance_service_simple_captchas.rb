require "httparty"

url = "https://rs.ap.gov.in/APCARDECClient/simpleCaptcha.jpg"

i = 83
loop do
  sleep(2.5)
  response = HTTParty.get(url)
  i = i + 1
  File.open(File.expand_path("./captchas/#{i}.jpg"), "w") do |file|
    file.puts(response.body)
  end
end

# Sseugi

  - Sseugi means "Writing" in Korean.
  - This is a De-Romanizer, based on the engine at http://www.mauvecloud.net/charsets/hangulgenerator.html
  - It does not work for obscure Roman characters, and older Jama are not produced yet.
  - I do not speak Korean, and therefore I am only as confident as the generator script above.
  - It needs help. It's not very good. It's very much in the Alpha stage.
  - Please feel free to leave requests to improve the project!

# How it Works

```
import sseugi
x = convert("igeos-eun siheom-ida")
print(x)

>> 익엇은 싷엄읻아
# It needs a lot of work, but the general idea is here
```
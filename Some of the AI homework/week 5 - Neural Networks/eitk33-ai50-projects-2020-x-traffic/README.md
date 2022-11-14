At first, I tried somewhat modest preferences. I began with 1 Convolutional layer, as well as 1 maxpool layer.
I noticed a very low accuracy rate - less than 0.1. From that point on I tried constantly improve the ML (machine learning).
starting with the Convolutional layer, I set the number of filters to be somewhat higher or lower, noticing
it didn't have that much of an effect. Afterwards i took the number of filters to be much lower (which made results worse),
but when the number of filters was reasonably higher (50 filters), i saw a noticeable improvement of the accuracy, 
as well as much longer processing time. later on I made some shifting to the Convolutional layer's kernel size, and it seems
as if there is an optimum between 3 and 6. higher, or lower, then those values, the accuracy went bad.
I then examined the effect of the mexpoll layer parameters; it turned out that the only value that managed to improve the accuracy
(initial kernel size was 3, 3) was 2, 2.

I sought to decrease the running time, so I tried to insert another Convolutional layer, resetting the 
first Convolutional layer to 36, and it's kernel to (5, 5). I also fixed the second Convolutional layer to those values.
I immediately noticed that while the accuracy didn't change much (with regarding the situation where there is only one
Convolutional layer with 50 filters), the running time indeed has been decreased. obviously, I decided to stay with 2 
Convolutional layer. trying to mimic the effect resulting from additional layer, I added another maxpool layer, but no 
matter how much I tried, I wasn't able to improve the results further. on the contrary - the accuracy has only gone
worse, regardless of the parameters applied to the maxpool layers. maxpool first layer size (MFLS) > maxpool first layer 
size (MSLS); MFLS < MSLS; MSLS = MSLS; MFLS >> MSLS; etc. so I decided to stay with one maxpool layer.

The last thing I tried was to increase the number of hidden layers. I thought that the only limitation would be the running time
that will increase with adding more layers. surprisingly enough, i also found out that there is an optimum range for the 
amount of hidden layers. (initially the number of layers was 128, then 250 and 300). after some optimization i fixed the 
number of hidden layers to 220. my last experiments were with the dropout value. i found out that increasing the dropout 
value (0.6) decreased the accuracy, while decreasing the dropout rate a bit (0.45) achieved better accuracy and lower 
loss. decreasing the dropout rate furthermore had a negative effect on the loss function

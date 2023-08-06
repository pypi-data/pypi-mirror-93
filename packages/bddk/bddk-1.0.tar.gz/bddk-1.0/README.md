# Bddk Data

This package helps you to collect your desired data from Bddk via selenium. 
Since this package automates browser, you do not need to use the interface of Bddk. 
Thus, ultimate aim is that one should able to get whatever data needed from Bddk without leaving python environment and visiting the 
site over and over again. 

### Prerequisites

OS - Windows, Linux or Mac

Browser - Chrome or Ubuntu

### Installing

Importing package should install all necessary files and programs for you.

In case of a problem;

[ChromeDriver](https://chromedriver.chromium.org/) for Chrome

[geckodriver](https://github.com/mozilla/geckodriver/releases) for Firefox

## Important Note

Both ChromeDriver and geckodriver are open source programs. They will be automatically installed on you computer and used accordingly.
However, Linux and Mac do not give permission to ChromeDriver for using Chrome. This package forces to run ChromeDriver program if that happens.

# How to Use

### Getting the Data

Returns dataframe

```
bddk.get_rapor(kalem, basyil, basay, bityil, bitay, per, para="TL", taraf=None, zaman=48, browser="firefox")

Paremeters:
    kalem : list, use get_kalem for suitable elements
        Kalemler
    basyil, bityil : str or int, year
        Baslangıç Yılı, Bitiş Yılı
    basay, bitay : str, months
        Baslangıç Ayı, Bitiş Ayı
    per : "3 Aylık", "6 Aylık", "Yıllık"
        Periyot
    para : "TL" (default), "USD" 
        Para Birimi
    taraf: list, use get_taraf for suitable elements
        Taraflar, "Sektör" her zaman seçilidir, bunun dışında istediklerinizi liste olarak ekleyin.
    zaman : int, 120 (default)
        Sitenin veya internetinizin durumuna göre paket zaman aşımına uğrayabilir. Yoğunluk durumunda arttırmanız tavsiye edilir.
    browser: "chrome" or "firefox"
        Kullandığınız web tarayıcı
```
#### Example
```
rapor = bddk.get_rapor(
    kalem=["Menkul Kıymetler-Finansman Bonoları", "Menkul Kıymetler-Hazine Bonoları"],
    basyil=2014,
    basay="Ocak",
    bityil=2020,
    bitay="Mart",
    per="1 Aylık",
    taraf=["Mevduat"],
    zaman=60,
    browser="chrome"
)
print(rapor.head())
```
### Getting Kalem and Taraf

Both functions print available strings and do not return any object. 
```
bddk.get_kalem(kalems=None, browser="firefox")

Parameters:
    kalems : str, returns full names of available kalem that consists of this string
        Kalem arama
    browser: "chrome" or "firefox"
        Kullandığınız web tarayıcı    

#######################################################

bddk.get_taraf(browser="firefox")
    
Parameters:
    browser: "chrome" or "firefox"
        Kullandığınız web tarayıcı  
```
#### Example
```
bddk.get_kalem("bono",browser="firefox")

bddk.get_taraf(browser="firefox")
```

## Authors

* **İlyas Burak Hızarcı** - [barbasan](https://github.com/barbasan)

## License

This project is licensed under the MIT License - see the [LICENSE.txt](LICENSE.txt) file for details


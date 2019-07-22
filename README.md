# finalprojectpwdk

Latar belakang project :
- Project ini dibuat sebagai salah satu ujian dalam mengikuti Program Job Connector - Data Science.

Project Deskripsi :
- Tema : Prediksi Harga Mobil Bekas
- Project ini dibuat berdasarkan data penjualan mobil di Ukraina pada tahun 2016.
- [Sumber dataset](https://www.kaggle.com/antfarol/car-sale-advertisements).

Project Handling :
- Dataset awal berisi 9500 lebih data penjualan mobil di Ukraina
- Setelah dilakukan cleaning dan checking, data bersih menjadi 9254 unit mobil
- Kemudian dilakukan pemodelan Mechine Learning, dengan 5 model sebagai model uji:
- Pengujian dilakukan dengan cross validation score, dengan hasil sbg berikut:

      ExtraTreesRegressor = [88.88024652 91.18600724 89.81385697 69.23091812 89.62042018] 85.75 %
      RandomForestRegressor = [88.40329223 92.41170237 87.98201626 77.20288853 89.01061405] 87.0 %
      GradientBoostingRegressor = [86.22765318 88.16413296 85.06291913 78.85929737 87.04884201] 85.07 %
      KNeighborsRegressor = [73.38962211 76.07419294 70.45501766 71.15131212 75.11656523] 73.24 %
      DecisionTreeRegressor = [60.89754438 81.01886923 78.65963687 70.37534232 79.46281232] 74.08 %
      
- Dari hasil pengujian maka dipilih model Random Forest Regressor. 
- Dengan model tsb, feature yang paling mempengaruhi adalah CarClass, Tahun Produksi, Volume mesin, jarak tempuh kendaraan.

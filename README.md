# AIoT_Final_Project - BurnSync
![BurnSync Image](/images/BurnSync.png)
* [Demo Videos](https://youtube.com/playlist?list=PL5VZWr9PWBnZU4I9REdP6TTMNPE_F1_AZ&si=Ig--suKz3TJ2gGJq)
## Authors
* Hsuan-Ying, Liu 
    * Affiliation: National Taiwan University, NTUEE
    * Email: stevenliu901205@gmail.com
    
* Chi-En Dai
    * Affiliation: National Taiwan University, NTUGICE
    * Email: dcn0629@gmail.com

**If you have any question about this project, do not hesitate to contact us for detail explanation!!!**
## Introduction
This is a final project for AIoT  course. Our project is **BurnSync**, which is a personal fitness assistant that can automatically track the number of repetitions and the number of sets during workout. It is a highly integrated system including both hardware and software. We made a custom website and deployed our classification model on Hugging Face. For more details, please refer to the slides we provide in the *slides* folder.
### Hardware
* Arduino Nano 33 BLE Sense Rev2 
(BurnSync Device)
* OLED module (SSD1306) 
* MAX30102 (heart beat module)
* Button
* 9V Battery
* Bread Board
* soft wires
* stretchy fabric
* Velcro

### Software
* Next.JS
* Firebase
* Hugging Face

## How to Use this Repository
1. Read our slides to understand the project
2. Try to make a BurnSync device by yourself, the materials is listed in the slides
3. Upload the code to the Arduino Nano board, the code is in *Arduino/Final.ino*
4. Visit our [website](https://burn-sync-website.vercel.app/sign-in), connect the device with the website through BLE
5. Start to do exercise
* notice: there are demo videos in the slides

## Related Repositories
* [Website](
https://github.com/lsy1205/BurnSync_website.git)
* [Huggging Face Repository](https://huggingface.co/spaces/AIOT12345/IMU_CLASSIFY)

## File Structure (Folders)
* Arduino: the Arduino code to upload to the Arduino Nano board
    * *data_collect.ino*: for collecting data to train model
    * *Final.ino*: the code for using the device
* Dataset: the dataset we used to train/test our model
* Machine Learning: the python code for training model
* Python: the python code to collect data, this folder will only be used when you want to collect your own data and train your own model
* Website: a simple html you can try with your own
* Slides: our presentation slides, you can also find demo videos in the slides
* Report: our project report, it is a detailed documentation
* Images: a folder to place images for README.md
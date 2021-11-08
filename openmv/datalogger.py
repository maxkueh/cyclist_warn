import sensor, image, pyb, time, fir

RED_LED_PIN = 1
BLUE_LED_PIN = 3
drawing_hint = image.BICUBIC

fir.init()
w = fir.width()*10
h = fir.height()*10

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)

rtc = pyb.RTC()
counter = 0

pyb.LED(RED_LED_PIN).on()
sensor.skip_frames(time = 2000)
pyb.LED(RED_LED_PIN).off()

def writeLog(timestamp, values):
    logline = ("%s;%s" % (timestamp, values))
    print(logline)

    try:
        with open("/mlxTemp.txt", "a") as f:
            f.write("\n%s" % logline)
            f.close()
            pyb.sync()

    except OSError as error:
        print("Error: can not write to SD card. %s" % error)

while(True):
    counter = counter + 1

    cameraImageName = "cam/cam_" + str(counter) + ".jpg"
    mlxImageName = "mlx/mlx_" + str(counter) + ".jpg"

    sensor.snapshot().save(cameraImageName)

    try:
        fir.snapshot(x_size=w, y_size=h, color_palette=fir.PALETTE_IRONBOW, hint=drawing_hint, copy_to_fb=True).save(mlxImageName)
    except OSError:
        continue
    try:
        ta, ir, to_min, to_max = fir.read_ir()
        writeLog(counter, ir)
    except OSError:
        continue

    time.sleep(1)

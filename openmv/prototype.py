import sensor, image, time, tf, pyb, fir

fir.init()
w = int(fir.width()*2.5)
h = int(fir.height()*2.5)

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_windowing((320,240))
sensor.skip_frames(time = 2000)

green_led = pyb.LED(2)

clock = time.clock()
counter = 0

net_cam = tf.load("model_quant_cam.tflite", load_to_fb=True)
net_mlx = tf.load("model_quant_mlx.tflite", load_to_fb=True)

labels = ['not_warn', 'warn']

drawing_hint = image.BICUBIC

def writeLog(timestamp, first_value, second_value):
    logline = ("%s;%s;%s" % (timestamp, first_value, second_value))

    try:
        with open("/classificationLog.txt", "a") as f:
            f.write("\n%s" % logline)
            f.close()
            pyb.sync()

    except OSError as error:
        print("Error: can not write to SD card. %s" % error)

while(True):
    clock.tick()
    green_led.on()
    green_led.off()
    counter = counter + 1

    img_cam = sensor.snapshot()

    cameraImageName = "cam/cam_" + str(counter) + ".jpg"
    img_cam.save(cameraImageName)

    try:
        img_mlx = fir.snapshot(x_size=w, y_size=h, color_palette=fir.PALETTE_IRONBOW, hint=drawing_hint, copy_to_fb=True)
    except OSError:
        continue

    mlxImageName = "mlx/mlx_" + str(counter) + ".jpg"
    img_mlx.save(mlxImageName)

    results_cam = net_cam.classify(img_cam)[0][4]
    results_mlx = net_mlx.classify(img_mlx)[0][4]

    print("warn (cam): " + str(results_cam[0]))
    print("warn (mlx): " + str(results_mlx[0]))

    writeLog(counter, results_cam[0], results_mlx[0])

    print(clock.fps(), "fps")

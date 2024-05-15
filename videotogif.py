import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import cv2
from PIL import Image, ImageTk

# TODO:
# 1. Bulk import/export and list of imported files
# 2. Choose between automatically export to the same directory or choose export location each time
# 3. Custom resizing
# 4. Working preview
# 5. Cropping
# 6. Make it prettier

class videoToGif(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("Video to GIF converter")
        self.geometry("400x300")
        self.resizable(False, False)

        self.inputPath = ""
        self.outputPath = ""
        self.frames = []
        self.previewFrameIndex = 0

        self.selectVideoBtn = tk.Button(self, text='Load video', command=self.loadVideo)
        self.selectVideoBtn.pack(pady=5)

        #self.previewLabel = tk.Label(self, text='Video preview')
        #self.previewLabel.pack(pady=5)

        #self.canvas = tk.Canvas(self, width=640, height=480, background='#eeeeee')
        #self.canvas.pack(pady=5)

        self.speedLabel = tk.Label(self, text='Speed (fps):')
        self.speedLabel.pack(pady=5)

        self.speedEntry = tk.Entry(self)
        self.speedEntry.pack(pady=5)
        self.speedEntry.insert(0, '12')

        self.scaleLabel = tk.Label(self, text='Scale:')
        self.scaleLabel.pack(pady=5)

        self.scaleEntry = tk.Entry(self)
        self.scaleEntry.pack(pady=5)
        self.scaleEntry.insert(0, '1.0')

        self.exportBtn = tk.Button(self, text='Export GIF', command=self.exportGif)
        self.exportBtn.pack(pady=5)

        self.progressBar = ttk.Progressbar(self, orient=tk.HORIZONTAL, length=130, mode='indeterminate')
        self.progressBar.pack(pady=5)
        

    def loadVideo(self):
        self.inputPath = filedialog.askopenfilename(title='Select video', filetypes=(('MP4 Files', '*.mp4'),('All files', '*.*')))
        if self.inputPath:
            self.processVideo()


    def processVideo(self):
        if not self.inputPath:
            return
        
        cap = cv2.VideoCapture(self.inputPath)
        self.frames = []

        while True:
            ret, frame = cap.read()
            
            if not ret:
                break

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.frames.append(frame)

        cap.release()

        self.previewFrameIndex = 0
        self.animatePreview()


    # def animatePreview(self):
    #     if not self.frames:
    #         return
        
    #     frame = self.frames[self.previewFrameIndex]
    #     frameImage = Image.fromarray(frame)
    #     frameImage = frameImage.resize((640, 480), Image.Resampling.LANCZOS)
    #     framePhoto = ImageTk.PhotoImage(frameImage)

    #     self.canvas.create_image(0, 0, anchor=tk.NW, image=framePhoto)
    #     self.canvas.image = framePhoto

    #     self.previewFrameIndex = (self.previewFrameIndex + 1) % len(self.frames)

    #     self.after(50, self.animatePreview)


    def exportGif(self):
        fps = int(self.speedEntry.get())
        scale = float(self.scaleEntry.get())

        if not self.frames or fps <= 0 or scale <= 0:
            messagebox.showerror('Error', 'Invalid options')
            return
        
        self.outputPath = filedialog.asksaveasfilename(defaultextension='.gif', filetypes=(('GIF Files', '*.gif'),('All files', '*.*')))

        if not self.outputPath:
            return
        
        self.progressBar.start(8)

        threading.Thread(target=self.createGif, args=(fps, scale), daemon=True).start()


    def createGif(self, fps, scale):
        outputFrames = []

        for frame in self.frames:
            img = Image.fromarray(frame)
            img = img.resize((int(img.width * scale), int(img.height * scale)), Image.Resampling.LANCZOS)
            outputFrames.append(img)

        outputFrames[0].save(self.outputPath, save_all=True, append_images=outputFrames[1:], optimize=False, duration=1000 // fps, loop=0)

        self.after(0, self.progressBar.stop)
        messagebox.showinfo('Success', 'GIF has been exported.')


if __name__ == '__main__':
    app = videoToGif()
    app.mainloop()
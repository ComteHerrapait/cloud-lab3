import matplotlib.pyplot as plt 
from PIL import Image

def imgProcess():
    # Open image by knowing path 
    img = Image.open("test.png")  
    
    # Convert to grayscale
    gray = img.convert('1')

    # Save the result in another file
    gray.save('result.png')

    # Plot both images
    fig, axes = plt.subplots(1, 2)
    ax = axes.ravel()

    ax[0].imshow(img)
    ax[0].set_title('Orginal')
    ax[1].imshow(gray, cmap=plt.cm.gray)
    ax[1].set_title('Grayscale')

    fig.tight_layout()
    plt.show()

imgProcess()
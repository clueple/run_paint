import cv2 
import streamlit as st 
import numpy as np 
import datetime as dt 

from PIL import Image



#current_time
now = dt.datetime.now().strftime('%x --- %X (%a)')

#reading image
# img_location = 'D:/edit_img/'
# #file_name
# filename = '014e.jpg'

# #define the image variable
# img = cv2.imread(img_location+filename)


'''
#Gray -> invert_gray -> blur_gray -> invert_blur -> divide_gray_by_invert_blur
'''


st.write(now)

# #gray the inmage
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# #blur the image
# gray_blur = cv2.GaussianBlur(gray, (25,25),50)

# #Convert the image into pencil sketch
# cartoon = cv2.divide(gray, gray_blur, scale=256.0)



def cartoonization(img, cartoon):
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	if cartoon == "Pencil Sketch":

		value = st.sidebar.slider('Tune the brightness of your sketch (higher value = brighter)',0.0, 300.0,250.0)
		kernel = st.sidebar.slider('Tune the boldness of the edges of your sketch (higher value = bolder edges)', 1,99, 25,step=2)

		gray_blur = cv2.GaussianBlur(gray, (kernel,kernel),0)

		cartoon = cv2.divide(gray, gray_blur, scale=value)

	if cartoon == 'Detail Enhancement':
		
		smooth = st.sidebar.slider('Tune the smoothness of the image (higher = smoother)', 3,99,5, step=2)
		kernel = st.sidebar.slider('Tune the sharpness of the image (lower = sharper)', 1,21,3, step=2)
		edge_preserve = st.sidebar.slider('Tune the color averaging effects (lower = only similar color be smoothed, high = dissimilar color be smoothed)', 0.0, 1.0, 0.5)

		gray = cv2.medianBlur(gray, kernel)	
		edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9,9)
		color = cv2.detailEnhance(img, sigma_s=smooth, sigma_r=edge_preserve)

		cartoon = cv2.bitwise_and(color, color, mask=edges)

	if cartoon == 'Pencil Edges':

		kernel = st.sidebar.slider('Tune the sharpness of the sketch (lower = sharper)',1,99,25,step=2)
		laplacian_filter = st.sidebar.slider('Tune the edge detection power (higher = more powerful', 3,9,3,step=2)
		noise_reduction = st.sidebar.slider('Tune the noise_effects of sketch (higher = noisier)',10,255,150)

		gray = cv2.medianBlur(gray, kernel)
		edges = cv2.Laplacian(gray, -1, ksize=laplacian_filter)
		edges_inv = 255 - edges

		dummy, cartoon = cv2.threshold(edges_inv, noise_reduction, 255, cv2.THRESH_BINARY)

	if cartoon == 'Bilateral Filter':

		smooth = st.sidebar.slider('Tune the smoothness of image (high = smoother )', 3,99,5, step=2)
		kernel = st.sidebar.slider('Tune the sharpness of image (low = sharper)', 1,21,3,step=2)
		edge_preserve = st.sidebar.slider('Tune the color averaging effects (low = similar color be smoothed; high = dissimilar color be smoothed)',1,100,50)

		gray = cv2.medianBlur(gray, kernel)
		edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,9,9)
    

		color = cv2.bilateralFilter(img, smooth, edge_preserve, smooth) 

		cartoon = cv2.bitwise_and(color, color, mask=edges)

	return cartoon

###         ###
st.write("""
	# Cartoonize Your Image.
	""")



file = st.sidebar.file_uploader('Upload an image', type = ['jpg','png'], encoding=None)


if file is None:
	st.text("You haven't uploaded an image.")

else:
	image = Image.open(file)
	img = np.array(image)

	option = st.sidebar.selectbox(
		'Select cartoon filters', ('Pencil Sketch', 'Detail Enhancement', 'Pencil Edges', 'Bilateral Filter')
		)

	st.text('Your original Image')
	st.image(image, use_column_width=True)

	st.text('Your Cartoonized Image')
	cartoon = cartoonization(img, option)

	st.image(cartoon, use_column_width=True)

# cv2.waitKey(0)
# cv2.destroyAllWindows()
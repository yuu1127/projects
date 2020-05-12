import numpy as np
import matplotlib.pyplot as plt
import cv2
import os
from skimage.feature import hog
from skimage import exposure
from sklearn import svm
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, accuracy_score, recall_score, confusion_matrix
import seaborn as sns

def load_images_from_folder(folder):
    images = []
    for filenames in os.listdir(folder):
        print(filenames)
        #filename.append(filenames)
        if filenames != '.DS_Store':
            for filename in os.listdir(folder + '/' + filenames):
                print(filename)
                img = cv2.imread(os.path.join(folder + '/' + filenames, filename), 0)
                #print(img)
                if img is not None:
                    images.append(img)
    return images

def main():
    train_dir = './train'
    train_n_dir = '/train_negative_A'
    train_n_dir_a = '/train_positive_A'
    train_n_dir_b = '/train_positive_B'
    train_n_dir_c = '/train_positive_C'
    train_n = load_images_from_folder(train_dir + train_n_dir)
    train_p = load_images_from_folder(train_dir + train_n_dir_a)
    train_p.extend(load_images_from_folder(train_dir + train_n_dir_b))
    train_p.extend(load_images_from_folder(train_dir + train_n_dir_c))

    test_n_dir = './test/test_negative'
    test_p_dir = './test/test_positive'
    test_n = load_images_from_folder(test_n_dir)
    test_p = load_images_from_folder(test_p_dir)
    # print(len(n_images))
    # print(len(p_images))
    X = []
    y = []
    hog_images = []
    # fd1, hog_image = hog(train_p[0], orientations=9, pixels_per_cell=(8, 8), cells_per_block=(2, 2), visualize=True)
    # # Rescale histogram for better display
    # hog_image_rescaled = exposure.rescale_intensity(hog_image, in_range=(0, 10))
    # plt.subplot(1, 2, 1), plt.imshow(train_p[0], cmap='gray'), plt.title('original')
    # plt.subplot(1, 2, 2), plt.imshow(hog_image_rescaled, cmap='gray'), plt.title('HOG')
    # plt.tight_layout()
    # plt.savefig("HOG1.png")
    # plt.show()

    for pos_roi in train_p:
        fd = hog(pos_roi, orientations=9, pixels_per_cell=(8, 8), cells_per_block=(2, 2), visualize=False)
        X.append(fd)
        y.append(1)
        #hog_images.append(hog_image)

    for neg_roi in train_n:
        fd = hog(neg_roi, orientations=9, pixels_per_cell=(8, 8), cells_per_block=(2, 2), visualize=False)
        X.append(fd)
        y.append(0)

    #plt.imshow(hog_images[51])



    ## covert list into numpy array
    X = np.array(X)
    y = np.array(y)
    print(X.shape)
    print(y.shape)


    print('start learning SVM.')
    lin_clf = svm.LinearSVC()
    lin_clf.fit(X, y)
    print('finish learning SVM.')

    X_test = []
    y_test = []
    for pos_roi in test_p:
        fd = hog(pos_roi, orientations=9, pixels_per_cell=(8, 8), cells_per_block=(2, 2), visualize=False)
        X_test.append(fd)
        y_test.append(1)

    for neg_roi in test_n:
        fd = hog(neg_roi, orientations=9, pixels_per_cell=(8, 8), cells_per_block=(2, 2), visualize=False)
        X_test.append(fd)
        y_test.append(0)


    y_pred1 = lin_clf.predict(X_test)
    print("SVM Accuracy: " + str(accuracy_score(y_test, y_pred1)))
    print('\n')
    print(classification_report(y_test, y_pred1))

    clf1 = DecisionTreeClassifier(max_depth=3)
    clf2 = KNeighborsClassifier(n_neighbors=5)
    clf3 = SGDClassifier(max_iter=1000, tol=1e-3)
    clf1.fit(X, y)
    clf2.fit(X, y)
    clf3.fit(X, y)

    y_pred2 = clf1.predict(X_test)
    # print("DT Accuracy: " + str(accuracy_score(y_test, y_pred2)))
    # print('\n')
    # print(classification_report(y_test, y_pred2))
    #
    y_pred3 = clf2.predict(X_test)
    # print("KN Accuracy: " + str(accuracy_score(y_test, y_pred3)))
    # print('\n')
    # print(classification_report(y_test, y_pred3))
    #
    y_pred4 = clf3.predict(X_test)
    # print("SGD Accuracy: " + str(accuracy_score(y_test, y_pred4)))
    # print('\n')
    # print(classification_report(y_test, y_pred4))

    average_precision1 = accuracy_score(y_test, y_pred1)
    average_precision2 = accuracy_score(y_test, y_pred2)
    average_precision3 = accuracy_score(y_test, y_pred3)
    average_precision4 = accuracy_score(y_test, y_pred4)
    recall1 = recall_score(y_test, y_pred1, average='macro')
    recall2 = recall_score(y_test, y_pred2, average='macro')
    recall3 = recall_score(y_test, y_pred3, average='macro')
    recall4 = recall_score(y_test, y_pred4, average='macro')

    print('COMP9517 Assignment2 z5186797')
    print('SVM Accuracy: {0:0.3f}    Recall: {0:0.3f}'.format(
        average_precision1, recall1))

    print('DT Accuracy: {0:0.3f}    Recall: {0:0.3f}'.format(
        average_precision2, recall2))

    print('KNN Accuracy: {0:0.3f}    Recall: {0:0.3f}'.format(
        average_precision3, recall3))

    print('SGD Accuracy: {0:0.3f}    Recall: {0:0.3f}'.format(
        average_precision4, recall4))

    cm = confusion_matrix(y_test, y_pred1)
    print(cm)
    sns.heatmap(cm, annot=True, cmap='Blues')
    plt.savefig('confusion_matrix.png')


if __name__ == '__main__':
    main()


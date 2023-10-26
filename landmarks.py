import bz2

compressed_file = 'shape_predictor_68_face_landmarks.dat.bz2'
extracted_file = 'shape_predictor_68_face_landmarks.dat'

with open(extracted_file, 'wb') as output_file, bz2.BZ2File(compressed_file, 'rb') as input_file:
    for data in iter(lambda: input_file.read(100 * 1024), b''):
        output_file.write(data)

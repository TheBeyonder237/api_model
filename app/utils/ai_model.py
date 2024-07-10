# app/utils/ai_model.py
import cv2
from ultralytics import YOLO


# app/utils/ai_model.py
import cv2
from ultralytics import YOLO


def process_video(input_video_path: str, output_video_path: str, model_path: str) -> float:
    cap = cv2.VideoCapture(input_video_path)
    ret, frame = cap.read()
    if not ret:
        raise Exception("Impossible de lire la vidéo")

    # Récupérez les dimensions d'origine de la vidéo
    H, W = frame.shape[:2]
    size = (W, H)
    out = cv2.VideoWriter(output_video_path, cv2.VideoWriter_fourcc(*'mp4v'), int(cap.get(cv2.CAP_PROP_FPS)), size)

    # Chargement du modèle personnalisé
    model = YOLO(model_path)
    threshold = 0.5
    max_score = 0.0  # Variable pour stocker la probabilité maximale

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame)[0]
        for result in results.boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = result
            if score > threshold:
                max_score = max(max_score, score)
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 4)
                label = f"{results.names[int(class_id)].upper()} - {score:.2f}"
                cv2.putText(frame, label, (int(x1), int(y1 - 10)), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3, cv2.LINE_AA)

        out.write(frame)

    cap.release()
    out.release()
    return max_score


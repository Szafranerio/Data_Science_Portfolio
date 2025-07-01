import torch
import torchvision.transforms as transforms
import torchvision.models as models
import cv2
import numpy as np

class CourtLineDetector:
    def __init__(self, model_path):
        self.model = models.resnet50(pretrained=False)
        self.model.fc = torch.nn.Linear(self.model.fc.in_features, 14 * 2)
        self.model.load_state_dict(torch.load(model_path, map_location='cpu'))
        self.model.eval()  # Set model to evaluation mode

        self.transform = transforms.Compose([
            transforms.ToPILImage(),
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
        
        # Initialize key_points attribute
        self.key_points = None  

    def predict(self, image):
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_tensor = self.transform(image_rgb).unsqueeze(0)

        with torch.no_grad():
            outputs = self.model(image_tensor)

        keypoints = outputs.squeeze().cpu().numpy()
        original_h, original_w = image.shape[:2]

        # Rescale keypoints back to the original image size
        keypoints[::2] *= original_w / 224.0
        keypoints[1::2] *= original_h / 224.0

        # Store the keypoints inside the object for future reference
        self.key_points = keypoints.reshape((-1, 2))  # Store as (x, y) pairs

        return keypoints

    def get_keypoints(self):
        """
        Returns the last detected keypoints.
        If `predict()` hasn't been run yet, returns None.
        """
        return self.key_points

    def draw_keypoints(self, image, keypoints=None):
        """
        Draws court keypoints on the image.
        Uses the last stored keypoints if none are provided.
        """
        if keypoints is None:
            keypoints = self.key_points  # Use stored keypoints if available

        if keypoints is not None:
            for i in range(0, len(keypoints), 2):
                x = int(keypoints[i])
                y = int(keypoints[i+1])
                
                cv2.putText(image, str(i//2), (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                cv2.circle(image, (x, y), 5, (0, 0, 255), -1)

        return image

    def draw_keypoints_on_video(self, video_frames, keypoints=None):
        """
        Draws court keypoints on each frame of the video.
        Uses stored keypoints if `keypoints` is not provided.
        """
        output_video_frames = []
        for frame in video_frames:
            frame = self.draw_keypoints(frame, keypoints)
            output_video_frames.append(frame)
        return output_video_frames

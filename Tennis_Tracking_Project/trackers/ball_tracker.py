from ultralytics import YOLO
import cv2
import pickle
import pandas as pd

class BallTracker:
    def __init__(self,model_path):
        self.model = YOLO(model_path)
        self.ball_trail = []
        
    def interpolate_ball_positions(self, ball_positions):
        ball_positions = [x.get(1,[]) for x in ball_positions]
        #Convert list to dataframe
        df_ball_positions = pd.DataFrame(ball_positions, columns=['x1', 'y1', 'x','y2'])
        
        #Interpolate missing values
        df_ball_positions = df_ball_positions.interpolate()
        df_ball_positions = df_ball_positions.bfill()
        
        ball_positions = [{1:x} for x in df_ball_positions.to_numpy().tolist()]

        return ball_positions
        
    def get_ball_shot_frames(self, ball_positions):
        #Convert list to dataframe
        ball_positions = [x.get(1,[]) for x in ball_positions]
        df_ball_positions = pd.DataFrame(ball_positions, columns=['x1', 'y1', 'x','y2'])
        
        df_ball_positions['ball_hit'] = 0
        
        df_ball_positions['mid_y'] = (df_ball_positions['y1'] + df_ball_positions['y2'])/2
        df_ball_positions['mid_y_rolling_mean'] = df_ball_positions['mid_y'].rolling(window=5, min_periods=1, center=False).mean()
        df_ball_positions['delta_y'] = df_ball_positions['mid_y_rolling_mean'].diff()  
        
        minimum_change_for_hit = 20
        for i in range(1,len(df_ball_positions) - int(minimum_change_for_hit*1.2)):
            negative_pos_change = df_ball_positions['delta_y'].iloc[i] > 0 and df_ball_positions['delta_y'].iloc[i+1] < 0
            positive_pos_change = df_ball_positions['delta_y'].iloc[i] < 0 and df_ball_positions['delta_y'].iloc[i+1] > 0

            if negative_pos_change or positive_pos_change:
                change_count = 0
                for change_frame in range (i+1, i+int(minimum_change_for_hit*1.2)+1):
                    negative_pos_change_following_frame = df_ball_positions['delta_y'].iloc[i] > 0 and df_ball_positions['delta_y'].iloc[change_frame] < 0
                    positive_pos_change_following_frame = df_ball_positions['delta_y'].iloc[i] < 0 and df_ball_positions['delta_y'].iloc[change_frame] > 0

                    if negative_pos_change and negative_pos_change_following_frame:
                        change_count += 1

                    elif positive_pos_change and positive_pos_change_following_frame:
                        change_count += 1 

                if change_count > minimum_change_for_hit - 1:
                    df_ball_positions.loc[i, 'ball_hit'] = 1  
        frame_nums_with_ball_hits = df_ball_positions[df_ball_positions['ball_hit']==1].index.tolist()   
        return frame_nums_with_ball_hits  
        
    def detect_frames(self,frames, read_from_stub=False, stub_path = None):
        ball_detections = []
        
        if read_from_stub and stub_path is not None:
            with open (stub_path, 'rb') as f:
                ball_detections = pickle.load(f)
            return ball_detections
        
        for frame in frames:
            player_dict = self.detect_frame(frame)
            ball_detections.append(player_dict)
            
        if stub_path is not None:
            with open(stub_path, 'wb') as f:
                pickle.dump(ball_detections, f)
            
        return ball_detections
        
    def detect_frame(self, frame):
        results = self.model.predict(frame, conf=0.01, iou=0.4)[0]
        

        ball_dict = {}
        min_area = float('inf')
        best_box = None

        for box in results.boxes:
            result = box.xyxy.tolist()[0]
            x1, y1, x2, y2 = result
            area = (x2 - x1) * (y2 - y1)

            if area < min_area:
                min_area = area
                best_box = result

        if best_box:
            ball_dict[1] = best_box
        else:
        
            if hasattr(self, "last_ball_box"):
                ball_dict[1] = self.last_ball_box

       

        return ball_dict

        
    

    def draw_bboxes(self, video_frames, ball_detections, trail_length=15):
        output_video_frames = []

        for frame, ball_dict in zip(video_frames, ball_detections):
            frame_copy = frame.copy()

            # Store current ball position in the trail
            if 1 in ball_dict:
                self.ball_trail.append(ball_dict[1])  
                
            if len(self.ball_trail) > trail_length:
                self.ball_trail.pop(0)  

            overlay = frame_copy.copy()

            # Draw fading ball shadow using circles
            for i, bbox in enumerate(self.ball_trail):
                x1, y1, x2, y2 = bbox
                cx, cy = int((x1 + x2) / 2), int((y1 + y2) / 2)
                radius = max(int((x2 - x1) / 2), 3) 
                alpha = (i + 1) / len(self.ball_trail)  
                color = (0, 255, 255) 

                cv2.circle(overlay, (cx, cy), radius, color, -1)
                overlay = cv2.addWeighted(overlay, alpha, frame_copy, 1 - alpha, 0)

            frame_copy = overlay

            # Draw the most recent ball position (sharp and clear)
            if 1 in ball_dict:
                x1, y1, x2, y2 = ball_dict[1]
                cx, cy = int((x1 + x2) / 2), int((y1 + y2) / 2)
                radius = max(int((x2 - x1) / 2), 3)
                cv2.circle(frame_copy, (cx, cy), radius, (0, 255, 255), -1)
                cv2.circle(frame_copy, (cx, cy), radius + 2, (0, 255, 255), 2)

            output_video_frames.append(frame_copy)

        return output_video_frames
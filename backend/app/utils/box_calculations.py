def box_area(box):
    x1, y1, x2, y2 = box
    return max(0.0, x2 - x1) * max(0.0, y2 - y1)

"""
def increase_box_height(text_box, bubble_box, factor):
    text_x1, text_y1, text_x2, text_y2 = text_box
    bubble_x1, bubble_y1, bubble_x2, bubble_y2 = bubble_box

"""


def shrink_box(box, shrink_factor=0.1):
    if not box:
         return None

    x1, y1, x2, y2 = box
    width = x2 - x1
    height = y2 - y1

    shrink_x = width * shrink_factor
    shrink_y = height * shrink_factor

    new_x1 = x1 + shrink_x
    new_y1 = y1 + shrink_y
    new_x2 = x2 - shrink_x
    new_y2 = y2 - shrink_y

    return [new_x1, new_y1, new_x2, new_y2]

# Return how many percentage of these two bounding boxes are overlapping
def iou(boxA, boxB):
	ax1, ay1, ax2, ay2 = boxA
	bx1, by1, bx2, by2 = boxB

	left = max(ax1, bx1)
	right = min(ax2, bx2)
	top = max(ay1, by1)
	bottom = min(ay2, by2)

	intersection_area = max(0, right - left) * max(0, bottom - top)

	area_a = box_area(boxA)
	area_b = box_area(boxB)

	union = area_a + area_b - intersection_area

	if union == 0:
		return 0.0 # Avoid dividing by 0 on the next line

	return intersection_area / union

# Find and group the bubble and text_bubble by their iou score and return them as a group of clusters
def group_by_iou(detections, iou_threshold=0.3):

    if not detections:
        return {}

    # indexes = sorted(range(len(detections)), key=lambda i: detections[i][1], reverse=True)
    used = set()
    clusters = {}

    for index, bubble_index in enumerate(detections):
        if bubble_index in used or detections[bubble_index]['label'] == 'text_bubble':
            continue

        cluster = {
        detections[bubble_index]['label']: detections[bubble_index]['coordinates']
        }

        used.add(bubble_index)

        for text_bubble_index in detections:
            if text_bubble_index in used or detections[text_bubble_index]['label'] == 'bubble':
                continue
            coordinatesA = detections[bubble_index]['coordinates']
            coordinatesB = detections[text_bubble_index]['coordinates']

            if iou(coordinatesA, coordinatesB) >= iou_threshold:
                cluster[detections[text_bubble_index]['label']] = detections[text_bubble_index]['coordinates']
                used.add(text_bubble_index)

            clusters[index] = cluster
            
    return clusters
class DataFormatter:

    def remove_and_total_tag_duplicates(tags: list) -> list:
        tag_data = {}

        for item in tags:
            tag = item['tag']
            confidence = float(item['confidence'])  # Convert confidence to float
            
            if tag in tag_data:
                tag_data[tag]['total_confidence'] += confidence
                tag_data[tag]['count'] += 1
            else:
                tag_data[tag] = {'total_confidence': confidence, 'count': 1}

        # Calculate the average confidence for each tag
        return [
            {'tag': tag, 'confidence': round(data['total_confidence'] / data['count'], 2)}
            for tag, data in tag_data.items()
    ]
        
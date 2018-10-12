import json
import os


def main():
    result = []
    research = []
    data = []
    chanel = []
    id = 0
    folders = os.listdir('/Users/kate_s/Desktop/PHYGITALISM/MLX/phyge/Resources/slack_history/')

    for folder in folders:
        if folder[0] != '.':
            files = os.listdir('/Users/kate_s/Desktop/PHYGITALISM/MLX/phyge/Resources/slack_history/' + folder)
            for file in files:
                with open('/Users/kate_s/Desktop/PHYGITALISM/MLX/phyge/Resources/slack_history/' + folder + '/' + file, 'r', encoding="utf8") as json_file:
                    research.append(json.load(json_file))
                data.append(file.replace('.json', ''))
                chanel.append(folder)

    for index, message in enumerate(research):
        attachments = message[0].get('attachments')
        if attachments and attachments[0].get('from_url'):
            result.append(dict(id=id,
                               data=data[index],
                               title=attachments[0].get('title'),
                               url=attachments[0].get('from_url'),
                               chanel=chanel[index]))
            id += 1

    with open('/Users/kate_s/Desktop/PHYGITALISM/MLX/phyge/Resources/slack_urls_handbook.json', 'w+', encoding="utf8") as file:
        json.dump(result, file, indent=2, ensure_ascii=False)


if __name__ == '__main__':
    main()

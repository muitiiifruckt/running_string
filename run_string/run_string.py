from PIL import Image, ImageDraw, ImageFont
import numpy as np
import moviepy.editor as mpy



# Ввод текста
text = input("Введите текст для бегущей строки: ")


# Функция для создания изображения с текстом
def create_text_image(text, font_size=50, padding=100):
    font = ImageFont.truetype("arial.ttf", font_size)
    text_width, text_height = font.getbbox(text)[2:4]

    # Увеличиваем высоту на дополнительное пространство снизу
    extra_height = font_size // 5  # Добавляем 20% от размера шрифта
    total_height = text_height + extra_height

    # Создаем изображение с увеличенной шириной и высотой (с дополнительным пространством перед и после текста)
    total_width = text_width + padding * 2
    image = Image.new('RGB', (total_width, total_height), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)

    # Рисуем текст на изображении с отступом слева на padding
    draw.text((padding, 0), text, font=font, fill=(0, 0, 0))

    return np.array(image)


# Функция для создания кадров бегущей строки
def create_frames(text, duration=3, fps=30):
    padding = 100  # Пространство перед и после текста
    image = create_text_image(text, padding=padding)
    h, w, _ = image.shape

    # Вычисляем количество кадров, чтобы текст успел пройти за 3 секунды
    total_frames = duration * fps

    frames = []

    # Скролл текста от пустого пространства слева до конца, когда весь текст выйдет за границы экрана
    for i in range(total_frames):
        # Прогресс сдвига текста: от -ширины текста до правого края экрана
        shift = int((w - padding) * (i / total_frames)) - (w - padding)
        frame = np.zeros((h, w, 3), dtype=np.uint8) + 255  # Белый фон
        frame[:, max(0, -shift):min(w, w - shift)] = image[:, max(0, shift):min(w, w + shift)]  # Перемещаем текст
        frames.append(frame)

    return frames


# Функция для создания видео из кадров
def create_scrolling_text_video(text, output_file=f'scrolling_text_{text}.mp4', duration=3, fps=30):
    frames = create_frames(text, duration, fps)
    clip = mpy.ImageSequenceClip(frames, fps=fps)
    clip.write_videofile(output_file, codec='libx264', fps=fps)


create_scrolling_text_video(text)

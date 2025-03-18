import os
import ffmpeg
import shutil
import asyncio
from fastapi import HTTPException

class Video:
    """Classe responsável pelo processamento de vídeos"""

    @staticmethod
    async def extract_frame(video_path: str, output_file: str, timestamp: int):
        """Extrai um frame do vídeo no tempo especificado"""
        try:
            print(f"📌 Extraindo frame em {timestamp}s para {output_file}...")
            await asyncio.to_thread(
                ffmpeg.input(video_path, ss=timestamp)
                .output(output_file, vframes=1)
                .overwrite_output()
                .run
            )
            print(f"✅ Frame salvo em {output_file}")
        except ffmpeg.Error as e:
            print(f"❌ Erro ao extrair frame: {e.stderr}")

    @staticmethod
    async def process_video(video_path: str, output_folder: str):
        """Executa o processamento do vídeo"""
        os.makedirs(output_folder, exist_ok=True)

        print(f"📌 Caminho do vídeo recebido: {video_path}")

        try:
            probe = await asyncio.to_thread(ffmpeg.probe, video_path)
        except ffmpeg.Error as e:
            print(f"❌ Erro ao rodar ffprobe: {e.stderr}")
            raise HTTPException(status_code=500, detail="Erro ao analisar vídeo com ffprobe")

        duration = float(probe['format']['duration'])
        interval = 20  

        tasks = []
        for i in range(0, int(duration), interval):
            output_file = os.path.join(output_folder, f'frame_at_{i}.jpg')
            tasks.append(Video.extract_frame(video_path, output_file, i))

        await asyncio.gather(*tasks)

        zip_path = output_folder + ".zip"
        await asyncio.to_thread(shutil.make_archive, base_name=output_folder, format='zip', root_dir=output_folder)

        return zip_path

from __future__ import print_function
import argparse
import torch
from PIL import Image
from torchvision.transforms import ToTensor
import numpy as np
import asyncio


async def doWork(pathInputPic, pathOutputPic, PATHtoMODEL):
    img = Image.open(pathInputPic).convert('YCbCr')
    y, cb, cr = img.split()
    model = torch.load(PATHtoMODEL)
    img_to_tensor = ToTensor()
    input = img_to_tensor(y).view(1, -1, y.size[1], y.size[0])
    #if opt.cuda:
    #    model = model.cuda()
    #    input = input.cuda()
    out = model(input)
    out = out.cpu()
    out_img_y = out[0].detach().numpy()
    out_img_y *= 255.0
    out_img_y = out_img_y.clip(0, 255)
    out_img_y = Image.fromarray(np.uint8(out_img_y[0]), mode='L')
    out_img_cb = cb.resize(out_img_y.size, Image.BICUBIC)
    out_img_cr = cr.resize(out_img_y.size, Image.BICUBIC)
    out_img = Image.merge('YCbCr', [out_img_y, out_img_cb, out_img_cr]).convert('RGB')
    out_img.save(pathOutputPic)


def main(pathInputPic, pathOutputPic, upscaleName, PATHtoMODEL):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(asyncio.new_event_loop())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(doWork(pathInputPic, pathOutputPic, PATHtoMODEL + '/' + upscaleName + '.pth'))
    loop.close()


if __name__ == "__main__":
    main()

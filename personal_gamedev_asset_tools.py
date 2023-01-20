#!/usr/bin/python3.9

# Features:
# Create sprite sheets using FFmpeg
# Recovers sprites (images) and sounds from a Game Maker Studio 2 project (tested only with GMS2 v2.2.5.481 projects)

import json
import time

from pathlib import Path
from sys import platform

if platform=="linux":
	import subprocess

def nice_digits(number_lim,number):
	output=str(number)
	lendiff=len(str(number_lim))-len(output)
	while lendiff>0:
		output="0"+output
		lendiff=len(str(number_lim))-len(output)

	return output

def copy(ipath,opath):
	with open(str(ipath),"rb") as ifile:
		with open(str(opath),"wb") as ofile:
			while True:
				chunk=ifile.read(1024*1024)
				if not chunk:
					break
				if chunk:
					ofile.write(chunk)

def create_odir(opath,name):
	odir=opath.joinpath(name)
	if odir.exists():
		odir=opath.joinpath(name+"."+time.strftime("%Y-%m-%d-%H-%M-%S"))

	odir.mkdir()
	return odir

def json_to_dict(json_file):
	json_ok={}
	json_raw=open(str(json_file)).read()
	json_raw=json_raw.strip()

	try:
		json_extracted=json.loads(json_raw)
	except Exception as e:
		print("Error (1) json_to_dict():",e)
	else:
		json_ok=json_extracted

	if not json_ok:
		true=True
		false=False
		null=None
		undefined=None

		try:
			assert json_raw.startswith("{") and json_raw.startswith("}")
			json_extracted=eval(json_raw)
		except Exception as e:
			print("Error (2) json_to_dict():",e)
		else:
			json_ok=json_extracted

	return json_ok

# Sprite Sheet Maker using FFmpeg
def util_ssm_ffmpeg(outdir,filename,the_list):
	print("\nUsing FFmpeg to create a sprite sheet...")

	issues=0

	the_suffix=the_list[0].suffix
	the_sheet=outdir.joinpath(filename+the_suffix)
	the_sheet_copy=outdir.joinpath(outdir.name+".copy"+the_suffix)

	idx=0
	for fse in the_list:
		idx=idx+1
		if idx==1:
			copy(fse,the_sheet)

		if idx>1:
			time.sleep(0.1)
			copy(the_sheet,the_sheet_copy)
			ffmpeg_line=["ffmpeg","-y","-v","warning","-i",str(the_sheet_copy),"-i",str(fse),"-filter_complex","hstack",str(the_sheet)]
			print("\nLine:",ffmpeg_line)
			sc=subprocess.run(ffmpeg_line).returncode
			print("Status Code:",sc)
			if (not sc==0):
				issues=issues+1

			ffmpeg_line.clear()

		if the_sheet_copy.exists():
			the_sheet_copy.unlink()

	return issues

def yy_recover_single_sound(opath,fse_list,yy_data):
	# TODO: Finish code for recovering sound files
	pass

def yy_recover_single_sprite(opath,fse_list,yy_data):

	if not ("frames" in yy_data):
		return

	if len(yy_data["frames"])==0:
		return

	asset_name=yy_data["name"]
	outdir=create_odir(opath,asset_name)

	recovered=0
	results={"total":len(yy_data["frames"]),"recovered":0}

	fse_list_final=[]

	index=0
	lastnum=len(yy_data["frames"])-1
	for frame in yy_data["frames"]:
		if "id" in frame:
			curr_id=frame["id"]
			for fse in fse_list:
				if fse.stem==curr_id:
					fse_rec_name=nice_digits(lastnum,index)
					fse_rec=outdir.joinpath(fse_rec_name+fse.suffix)
					if fse.exists():
						copy(fse,fse_rec)
						fse_list_final.append(fse_rec)

					break

			index=index+1

	recov=len(fse_list_final)
	results["recov"]=recov

	if platform=="linux" and len(fse_list_final)>1:
		if not (subprocess.run(["which","ffmpeg"]).returncode==0):
			print("FFmpeg not found: cannot create a sprite sheet")
			return results

		errors_found=util_ssm_ffmpeg(outdir,asset_name,fse_list_final)
		results.update({"ssm_errors":errors_found})

	return results

def yy_recover_single(opath,yy_res_dir):

	if type(opath) is str:
		opath=Path(opath)

	opath.mkdir(parents=True,exist_ok=True)

	if type(yy_res_dir) is str:
		yy_res_dir=Path(yy_res_dir)

	fse_list=list(yy_res_dir.glob("*"))
	for fse in fse_list:
		if fse.name==yy_res_dir.name+".yy":
			fse_yy_json=fse
			break

	if not fse_yy_json:
		return

	yy_data=json_to_dict(fse_yy_json)
	if not yy_data:
		return

	if not ("name" in yy_data):
		return

	if not ("modelName" in yy_data):
		return

	if not (yy_data["modelName"] in ["GMSprite","GMSound"]):
		return

	if yy_data["modelName"]=="GMSprite":
		results=yy_recover_single_sprite(opath,fse_list,yy_data)

	if yy_data["modelName"]=="GMSound":
		# results=yy_recover_single_sound(opath,fse_list,yy_data)
		results=False

	return results

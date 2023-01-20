#!/usr/bin/python3.9

# Recovers sprites (images) and sounds from a Game Maker Studio 2 project
# Tested on projects made with GMS2 v2.2.5.481

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

def yy_json_readfile(yy_json_file):
	json_ok={}
	json_raw=open(str(yy_json_file)).read()
	json_raw=json_raw.strip()

	try:
		json_extracted=json.loads(json_raw)
	except Exception as e:
		print("Error (1) yy_json_getfile():",e)
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
			print("Error (2) yy_json_getfile():",e)
		else:
			json_ok=json_extracted

	return json_ok

def yy_json_getfile(fse_list,yy_dir):
	target_name=yy_dir.name+".yy"
	for fse in fse_list:
		if fse.name==target_name:
			return fse

	return None

def recover_single_sound(opath,fse_list,yy_data):
	# TODO: Finish code for recovering sound files
	pass

def recover_single_sprite(opath,fse_list,yy_data):

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

		print("Using FFmpeg to create a sprite sheet...")
		results.update({"sheet_problem":False})
		the_suffix=fse_list_final[0].suffix
		the_sheet=outdir.joinpath(asset_name+the_suffix)
		the_sheet_copy=outdir.joinpath(outdir.name+".backup"+the_suffix)

		# row_files=[]
		# row_limit=5

		idx=0
		for fse in fse_list_final:
			idx=idx+1
			if idx==1:
				copy(fse,the_sheet)
				#row_files.append(fse)
				#print(idx,"$ copy 'the_sheet'")

			if idx>1:
				copy(the_sheet,the_sheet_copy)

				ffmpeg_line=["ffmpeg","-y","-v","warning","-i",str(the_sheet_copy),"-i",str(fse),"-filter_complex"]
				ffmpeg_line.append("hstack")
				#if len(row_files)>0:
				#	ffmpeg_line.append("hstack")
				#if len(row_files)==0:
				#	ffmpeg_line.append("vstack")

				ffmpeg_line.append(str(the_sheet))
				#print(idx,"$",ffmpeg_line)

				#row_files.append(fse)
				#if len(row_files)==row_limit:
				#	row_files.clear()

				time.sleep(0.1)
				print("\nLine:",ffmpeg_line)
				sc=subprocess.run(ffmpeg_line).returncode
				print("Status Code:",sc)
				if not sc==0 and results["sheet_problem"]==False:
					results["sheet_problem"]=True

				ffmpeg_line.clear()

		if the_sheet_copy.exists():
			the_sheet_copy.unlink()

	return results

# All functions below this point can be used individually

def recover_single(opath,yy_res_dir):

	if type(opath) is str:
		opath=Path(opath)

	opath.mkdir(parents=True,exist_ok=True)

	if type(yy_res_dir) is str:
		yy_res_dir=Path(yy_res_dir)

	fse_list=list(yy_res_dir.glob("*"))
	fse_yy_json=yy_json_getfile(fse_list,yy_res_dir)

	if not fse_yy_json:
		return

	yy_data=yy_json_readfile(fse_yy_json)
	if not yy_data:
		return

	if not ("name" in yy_data):
		return

	if not ("modelName" in yy_data):
		return

	if not (yy_data["modelName"] in ["GMSprite","GMSound"]):
		return

	if yy_data["modelName"]=="GMSprite":
		results=recover_single_sprite(opath,fse_list,yy_data)

	if yy_data["modelName"]=="GMSound":
		# results=recover_single_sound(opath,fse_list,yy_data)
		results=False

	return results

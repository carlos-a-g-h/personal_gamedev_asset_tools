#!/usr/bin/python3.9

import json
import time

from pathlib import Path
from sys import platform

#try:
#	from bs4 import BeautifulSoup
#except:
#	print("\nWARNING: You don't have BeautifulSoup installed")

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

def pathlib_cult(gpath):
	if type(gpath) is str:
		return Path(gpath)

	return gpath

def kill_extra_spaces(text_raw):
	text_raw=text_raw.strip()
	text_split=text_raw.split()
	text_list=[]
	for part_raw in text_split:
		part=part_raw.strip()
		if len(part)>0:
			text_list.append(part)

	return text_list

def path_force(opath,name,sfx=None):
	n=name
	if sfx:
		n=n+sfx
	the_path=opath.joinpath(n)
	if the_path.exists():
		n=name+"."+time.strftime("%Y-%m-%d-%H-%M-%S")
		if sfx:
			n=n+sfx
		the_path=opath.joinpath(n)

	return the_path

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

# Utility (misc): Create a sprite sheet using FFmpeg
def ssm_ffmpeg(outdir,filename,the_list):
	print("\nUsing FFmpeg to create a sprite sheet...")

	issues=0
	framecount=str(len(the_list))+"f"

	outdir=pathlib_cult(outdir)

	the_suffix=the_list[0].suffix
	the_sheet=outdir.joinpath(filename+"_"+framecount+the_suffix)
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

# Utility (GMS2): Recover single sound resource
def yyz_recover_single_sound(opath,fse_list,yy_data):
	opath=pathlib_cult(opath)
	asset_name=yy_data["name"]
	ofile=path_force(opath,asset_name,".ogg")
	for fse in fse_list:
		if fse.name==asset_name:
			copy(fse,ofile)
			break

	if ofile.exists():
		return True

	return False

# Utility (GMS2): Recover single sprite resource
def yyz_recover_single_sprite(opath,fse_list,yy_data):

	if not ("frames" in yy_data):
		return

	if len(yy_data["frames"])==0:
		return

	asset_name=yy_data["name"]
	outdir=path_force(opath,asset_name)
	outdir.mkdir()

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

		errors_found=ssm_ffmpeg(outdir,asset_name,fse_list_final)
		results.update({"ssm_errors":errors_found})

	return results

# Utility (GMS2): Recover single resource (sprite or sound)
def yyz_recover_single(opath,yy_dir_res):

	if type(opath) is str:
		opath=Path(opath)

	opath.mkdir(parents=True,exist_ok=True)

	if type(yy_dir_res) is str:
		yy_dir_res=Path(yy_dir_res)

	fse_list=list(yy_dir_res.glob("*"))
	for fse in fse_list:
		if fse.name==yy_dir_res.name+".yy":
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
		results=yyz_recover_single_sprite(opath,fse_list,yy_data)

	if yy_data["modelName"]=="GMSound":
		results=yyz_recover_single_sound(opath,fse_list,yy_data)

	return results

# Utility (GMS2): [WIP]
def yyz_recover(opath,yy_dir_cat):
	pass

# Utility (GM): Convert Game maker 3D model (D3D gmmod) to OBJ file format
def gm3df_to_obj(opath,infile):

	opath=pathlib_cult(opath)
	infile=pathlib_cult(infile)

	compat=False
	fmt=infile.suffix.lower()
	if "gmmod" in fmt:
		compat=True
		line_col=open(str(infile)).readlines()

	#if "gml" in fmt:
	#	compat=True
	#	line_col=gml_to_gmmod_data(infile)

	if not compat:
		return {}

	obj_v=""
	obj_vt=""
	obj_vn=""
	vcount=0

	obj_f=""
	obj_f_buff=""
	fcount=0

	for line_raw in line_col:

		if "gmmod" in fmt:
			line=kill_extra_spaces(line_raw)
			if not (len(line)==11):
				continue

			if not ("9" in line[0]):
				continue

			try:
				assert int(line[0])==9
			except:
				continue

			x,y,z,nx,ny,nz,xtex,ytex=line[1:-2]

		if "gml" in fmt:
			x,y,z,nx,ny,nz,xtex,ytex=line_raw

		vcount=vcount+1

		obj_v=obj_v+"\nv "+x+" "+y+" "+z+" 1.0"
		obj_vt=obj_vt+"\nvt "+xtex+" "+ytex
		obj_vn=obj_vn+"\nvn "+nx+" "+ny+" "+nz

		if fcount==0:
			obj_f_buff="f"
		fcount=fcount+1
		obj_f_buff=obj_f_buff+" "+str(vcount)+"/"+str(vcount)+"/"+str(vcount)
		if fcount==3:
			fcount=0
			obj_f=obj_f+"\n"+obj_f_buff

	if len(obj_v)>0 and len(obj_vt)>0 and len(obj_vn)>0 and len(obj_f)>0:

		file_obj=path_force(opath,infile.stem,".obj")
		file_mtl=opath.joinpath(file_obj.stem+".mtl")

		mtl_cont="# MTL generated by util_gm3df_to_obj()"
		mtl_cont=mtl_cont+"\n# From \""+str(infile.name)+"\"\n# To \""+str(file_mtl.name)+"\"\n"
		mtl_cont=mtl_cont+"\nnewmtl Material\nKd 1 1 1\nd 1"
		open(str(file_mtl),"wt").write(mtl_cont)

		obj_cont="# OBJ generated by util_gm3df_to_obj()"
		obj_cont=obj_cont+"\n# From \""+str(infile.name)+"\"\n# To \""+str(file_obj.name)+"\"\n"
		obj_cont=obj_cont+"\nmtllib "+file_mtl.name+"\nusemtl Material"
		obj_cont=obj_cont+"\n"+obj_v+"\n"+obj_vt+"\n"+obj_vn+"\n\ns off\n"+obj_f
		open(str(file_obj),"wt").write(obj_cont)

		return {"obj":file_obj,"mtl":file_mtl}

	return {}

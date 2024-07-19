<?xml version='1.0' encoding='UTF-8'?>
<Project Type="Project" LVVersion="24008000">
	<Property Name="NI.LV.All.SourceOnly" Type="Bool">true</Property>
	<Item Name="My Computer" Type="My Computer">
		<Property Name="server.app.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="server.control.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="server.tcp.enabled" Type="Bool">false</Property>
		<Property Name="server.tcp.port" Type="Int">0</Property>
		<Property Name="server.tcp.serviceName" Type="Str">My Computer/VI Server</Property>
		<Property Name="server.tcp.serviceName.default" Type="Str">My Computer/VI Server</Property>
		<Property Name="server.vi.callsEnabled" Type="Bool">true</Property>
		<Property Name="server.vi.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="specify.custom.address" Type="Bool">false</Property>
		<Item Name="Python文件调用.vi" Type="VI" URL="../../Python文件调用.vi"/>
		<Item Name="大刘.ico" Type="Document" URL="/E/桌面/项目/my_gpt8K_3/Labview/大刘.ico"/>
		<Item Name="大刘蓝.ico" Type="Document" URL="/E/桌面/项目/my_gpt8K_3/Labview/大刘蓝.ico"/>
		<Item Name="界面.vi" Type="VI" URL="../../界面.vi"/>
		<Item Name="屏幕截图 2024-07-18 203827.ico" Type="Document" URL="/E/桌面/屏幕截图 2024-07-18 203827.ico"/>
		<Item Name="Dependencies" Type="Dependencies">
			<Item Name="vi.lib" Type="Folder">
				<Item Name="Error Cluster From Error Code.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Error Cluster From Error Code.vi"/>
				<Item Name="Open Anaconda Python Session.vi" Type="VI" URL="/&lt;vilib&gt;/Python/Open Anaconda Python Session.vi"/>
				<Item Name="Open Venv Python Session.vi" Type="VI" URL="/&lt;vilib&gt;/Python/Open Venv Python Session.vi"/>
				<Item Name="Open Virtual Environment Session.vi" Type="VI" URL="/&lt;vilib&gt;/Python/Open Virtual Environment Session.vi"/>
			</Item>
		</Item>
		<Item Name="Build Specifications" Type="Build">
			<Item Name="BigLiuGPT" Type="EXE">
				<Property Name="App_copyErrors" Type="Bool">true</Property>
				<Property Name="App_INI_aliasGUID" Type="Str">{E128538F-9E72-4807-B2AE-A850641D3EAA}</Property>
				<Property Name="App_INI_GUID" Type="Str">{C68A70DD-815D-4938-8D33-C4A234763C8B}</Property>
				<Property Name="App_serverConfig.httpPort" Type="Int">8002</Property>
				<Property Name="App_serverType" Type="Int">0</Property>
				<Property Name="Bld_autoIncrement" Type="Bool">true</Property>
				<Property Name="Bld_buildCacheID" Type="Str">{6AF02A0D-F331-4844-87F1-BB2A4618AE51}</Property>
				<Property Name="Bld_buildSpecName" Type="Str">BigLiuGPT</Property>
				<Property Name="Bld_excludeInlineSubVIs" Type="Bool">true</Property>
				<Property Name="Bld_excludeLibraryItems" Type="Bool">true</Property>
				<Property Name="Bld_excludePolymorphicVIs" Type="Bool">true</Property>
				<Property Name="Bld_localDestDir" Type="Path">../builds/NI_AB_PROJECTNAME/BigLiuGPT</Property>
				<Property Name="Bld_localDestDirType" Type="Str">relativeToCommon</Property>
				<Property Name="Bld_modifyLibraryFile" Type="Bool">true</Property>
				<Property Name="Bld_previewCacheID" Type="Str">{51ECBB25-5EE4-4EEB-BBD0-AB89B9741860}</Property>
				<Property Name="Bld_version.build" Type="Int">6</Property>
				<Property Name="Bld_version.major" Type="Int">1</Property>
				<Property Name="Destination[0].destName" Type="Str">BigLiuGPT.exe</Property>
				<Property Name="Destination[0].path" Type="Path">../builds/NI_AB_PROJECTNAME/BigLiuGPT/BigLiuGPT.exe</Property>
				<Property Name="Destination[0].preserveHierarchy" Type="Bool">true</Property>
				<Property Name="Destination[0].type" Type="Str">App</Property>
				<Property Name="Destination[1].destName" Type="Str">Support Directory</Property>
				<Property Name="Destination[1].path" Type="Path">../builds/NI_AB_PROJECTNAME/BigLiuGPT/data</Property>
				<Property Name="DestinationCount" Type="Int">2</Property>
				<Property Name="Exe_iconItemID" Type="Ref">/My Computer/大刘蓝.ico</Property>
				<Property Name="Source[0].itemID" Type="Str">{E286063F-1F0B-4E22-B815-0BF133DC61CB}</Property>
				<Property Name="Source[0].type" Type="Str">Container</Property>
				<Property Name="Source[1].destinationIndex" Type="Int">0</Property>
				<Property Name="Source[1].itemID" Type="Ref">/My Computer/界面.vi</Property>
				<Property Name="Source[1].sourceInclusion" Type="Str">TopLevel</Property>
				<Property Name="Source[1].type" Type="Str">VI</Property>
				<Property Name="Source[2].destinationIndex" Type="Int">0</Property>
				<Property Name="Source[2].itemID" Type="Ref">/My Computer/Python文件调用.vi</Property>
				<Property Name="Source[2].sourceInclusion" Type="Str">Include</Property>
				<Property Name="Source[2].type" Type="Str">VI</Property>
				<Property Name="SourceCount" Type="Int">3</Property>
				<Property Name="TgtF_fileDescription" Type="Str">BigLiuGPT</Property>
				<Property Name="TgtF_internalName" Type="Str">BigLiuGPT</Property>
				<Property Name="TgtF_legalCopyright" Type="Str">Copyright ?2024 </Property>
				<Property Name="TgtF_productName" Type="Str">BigLiuGPT</Property>
				<Property Name="TgtF_targetfileGUID" Type="Str">{DF899F1B-EC7B-439F-B6C3-82E8D9BCD9A2}</Property>
				<Property Name="TgtF_targetfileName" Type="Str">BigLiuGPT.exe</Property>
				<Property Name="TgtF_versionIndependent" Type="Bool">true</Property>
			</Item>
		</Item>
	</Item>
</Project>

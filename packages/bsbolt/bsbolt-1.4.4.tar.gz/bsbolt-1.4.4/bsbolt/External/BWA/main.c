#include <stdio.h>
#include <string.h>
#include "kstring.h"
#include "utils.h"

#ifndef PACKAGE_VERSION
#define PACKAGE_VERSION "BSB-1.2.1-BWA-fork-0.7.17"
#endif

int bwa_index(int argc, char *argv[]);



int main_mem(int argc, char *argv[]);

	
static int usage()
{
	fprintf(stderr, "\n");
	fprintf(stderr, "Program: bwa (alignment via Burrows-Wheeler transformation)\n");
	fprintf(stderr, "Version: %s\n", PACKAGE_VERSION);
	fprintf(stderr, "Usage:   bwa <command> [options]\n\n");
	fprintf(stderr, "Command: index         index sequences in the FASTA format\n");
	fprintf(stderr, "         mem           BWA-MEM algorithm\n");
	fprintf(stderr, "\n");
	fprintf(stderr, "\n");
	fprintf(stderr,
"Note: To use BWA, you need to first index the genome with `bwa index'.\n"
"      There are three alignment algorithms in BWA: `mem', `bwasw', and\n"
"      `aln/samse/sampe'. If you are not sure which to use, try `bwa mem'\n"
"      first. Please `man ./bwa.1' for the manual.\n\n");
	return 1;
}

int main(int argc, char *argv[])
{
	extern char *bwa_pg;
	int i, ret;
	double t_real;
	kstring_t pg = {0,0,0};
	t_real = realtime();
	ksprintf(&pg, "@PG\tID:bwa\tPN:bwa\tVN:%s\tCL:%s", PACKAGE_VERSION, argv[0]);
	for (i = 1; i < argc; ++i) ksprintf(&pg, " %s", argv[i]);
	bwa_pg = pg.s;
	if (argc < 2) return usage();
    if (strcmp(argv[1], "index") == 0) ret = bwa_index(argc-1, argv+1);
	else if (strcmp(argv[1], "mem") == 0) ret = main_mem(argc-1, argv+1);
	else {
		fprintf(stderr, "[main] unrecognized command '%s'\n", argv[1]);
		return 1;
	}
	err_fflush(stdout);
	err_fclose(stdout);
	if (ret == 0) {
		fprintf(stderr, "[%s] Version: %s\n", __func__, PACKAGE_VERSION);
		fprintf(stderr, "[%s] CMD:", __func__);
		for (i = 0; i < argc; ++i)
			fprintf(stderr, " %s", argv[i]);
		fprintf(stderr, "\n[%s] Real time: %.3f sec; CPU: %.3f sec\n", __func__, realtime() - t_real, cputime());
	}
	free(bwa_pg);
	return ret;
}
